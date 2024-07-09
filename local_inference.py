import asyncio
import json
import pandas as pd
import torch
import numpy as np
import random
import websockets
from datetime import time
import h5py
import argparse

# 加载预测模型相关的模块
import util
from engine import trainer

# 加载数据文件
file = 'C:\\Users\\86133\\Downloads\\pems-bay.h5'
f = h5py.File(file, 'r')
sensor_ids = f['speed']['axis0'][:]
datetimes = pd.to_datetime(f['speed']['axis1'][:])
speed_data = f['speed']['block0_values'][:]

# 读取街道数据
with open('sorted_sensor_street.json', 'r') as file:
    street_data = json.load(file)

# 初始化 averageSpeeds
average_speeds = {int(sensor_id): {'totalSpeed': 0, 'count': 0} for sensor_id in sensor_ids}

def get_time_step(predict_time):
    time_steps = {'15min': 3, '30min': 6, '1h': 12}
    if predict_time in time_steps:
        return time_steps[predict_time]
    else:
        raise ValueError("Invalid predict time. Choose from '15min', '30min', '1h'.")

def set_random_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)

def load_data_and_supports(data_path, adjdata, adjtype, device, batch_size):
    sensor_ids, sensor_id_to_ind, adj_mx = util.load_adj(adjdata, adjtype)
    dataloader = util.load_dataset(data_path, batch_size, batch_size, batch_size)
    scaler = dataloader['scaler']
    return dataloader, scaler

def load_model(args, device, scaler):
    model = trainer(scaler,
                    in_dim=args.in_dim,
                    seq_length=args.seq_length,
                    num_nodes=args.num_nodes,
                    nhid=args.nhid,
                    dropout=args.dropout,
                    device=device,
                    lr_mul=args.lr_mul,
                    n_warmup_steps=args.n_warmup_steps,
                    quantile=args.quantile,
                    is_quantile=args.is_quantile,
                    warmup_epoch=args.warmup_epoch).model
    model.load_state_dict(torch.load(args.load_path, map_location=device))
    model.to(device)
    model.eval()
    return model

def main(predict_time, args):
    set_random_seed(args.seed)
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    dataloader, scaler = load_data_and_supports(args.data, args.adjdata, args.adjtype, device, args.batch_size)
    model = load_model(args, device, scaler)
    time_step = get_time_step(predict_time)

    all_batches = list(enumerate(dataloader['val_loader'].get_iterator()))
    selected_batch = random.choice(all_batches)
    iter, (x, y) = selected_batch

    results = []
    with torch.no_grad():
        testx = torch.Tensor(x).to(device).transpose(1, 3)[:, :, :, -24:]
        preds = model(testx)[:, :, :, time_step - 1]
        results.append(preds.cpu().numpy())

    return results[0][0]

async def send_data(websocket, path):
    # 初始化参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda:0', help='Device to use for computation')
    parser.add_argument('--data', type=str, default='data/PEMS-BAY', help='Data path')
    parser.add_argument('--adjdata', type=str, default='data/PEMS-BAY/adj_mx.pkl', help='Adjacency data path')
    parser.add_argument('--adjtype', type=str, default='doubletransition', help='Adjacency type')
    parser.add_argument('--seq_length', type=int, default=12, help='Sequence length')
    parser.add_argument('--nhid', type=int, default=32, help='Number of hidden units')
    parser.add_argument('--in_dim', type=int, default=2, help='Input dimension')
    parser.add_argument('--num_nodes', type=int, default=325, help='Number of nodes')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--dropout', type=float, default=0.3, help='Dropout rate')
    parser.add_argument('--seed', type=int, default=99, help='Random seed')
    parser.add_argument('--load_path', type=str,
                        default='E:/training/1/traffic-forcast-backend-main/model/TESTAM/model pth/BEST_PEMS-BAY_1.55.pth')
    parser.add_argument('--lr_mul', type=float, default=1, help='Learning rate multiplier')
    parser.add_argument('--n_warmup_steps', type=int, default=4000, help='Number of warm-up steps')
    parser.add_argument('--quantile', type=float, default=0.7, help='Quantile value')
    parser.add_argument('--is_quantile', action='store_true', help='Use quantile regression')
    parser.add_argument('--warmup_epoch', type=int, default=0, help='Number of warm-up epochs')
    args = parser.parse_args([])

    time_step = 0
    total_steps = len(datetimes)

    while True:
        predict_time = '15min'  # 设置预测时间间隔
        preds = main(predict_time, args)

        sensor_data = []
        for s, sensor_id in enumerate(sensor_ids):
            speed = preds[s]
            average_speeds[int(sensor_id)]['totalSpeed'] += speed
            average_speeds[int(sensor_id)]['count'] += 1
            sensor_data.append({
                'sensor_id': int(sensor_id),
                'speed': speed,
                'timestamp': str(datetimes[time_step])
            })

        street_averages = {}
        for street, sensors in street_data.items():
            speeds = [preds[list(sensor_ids).index(sensor_id)] for sensor_id in sensors if sensor_id in sensor_ids]
            if speeds:
                street_averages[street] = sum(speeds) / len(speeds)
            else:
                street_averages[street] = None

        sorted_street_averages = sorted(street_averages.items(),
                                        key=lambda x: x[1] if x[1] is not None else -float('inf'), reverse=True)[:10]
        sorted_street_averages = dict(sorted_street_averages)

        total_speed = sum([data['totalSpeed'] for data in average_speeds.values()])
        total_count = sum([data['count'] for data in average_speeds.values()])
        overall_average_speed = total_speed / total_count if total_count != 0 else 0

        response = json.dumps({
            'sensor_data': sensor_data,
            'street_averages': sorted_street_averages,
            'overall_average_speed': overall_average_speed
        })

        await websocket.send(response)
        print(f"Sent data for time_step: {time_step}")

        time_step = (time_step + 1) % total_steps  # 循环数据
        await asyncio.sleep(1)  # 每一秒发送一次数据

start_server = websockets.serve(send_data, "localhost", 5002)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
