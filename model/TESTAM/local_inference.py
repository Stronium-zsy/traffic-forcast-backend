import argparse
import pandas as pd
from datetime import time as dtime
import torch
import numpy as np
import util
from engine import trainer
import random
import time
from flow_pre.flowUtil import forecast_flow


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
    supports = [torch.tensor(i).to(device) for i in adj_mx]
    dataloader = util.load_dataset(data_path, batch_size, batch_size, batch_size)
    scaler = dataloader['scaler']
    return dataloader, scaler, supports


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


def main(time):
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda:0', help='Device to use for computation')
    parser.add_argument('--data', type=str, default='data/PEMS-BAY', help='Data path')
    parser.add_argument('--adjdata', type=str, default='data/PEMS-BAY/adj_mx.pkl', help='Adjacency data path')
    parser.add_argument('--adjtype', type=str, default='doubletransition', help='Adjacency type')
    parser.add_argument('--seq_length', type=int, default=12, help='Sequence length')
    parser.add_argument('--nhid', type=int, default=32, help='Number of hidden units')
    parser.add_argument('--in_dim', type=int, default=2, help='Input dimension')
    parser.add_argument('--num_nodes', type=int, default=325, help='Number of nodes')
    parser.add_argument('--batch_size', type=int, default=1, help='Batch size')
    parser.add_argument('--dropout', type=float, default=0.3, help='Dropout rate')
    parser.add_argument('--seed', type=int, default=99, help='Random seed')
    parser.add_argument('--load_path', type=str,
                        default='model_pth/BEST_PEMS-BAY_1.19.pth')
    parser.add_argument('--lr_mul', type=float, default=1, help='Learning rate multiplier')
    parser.add_argument('--n_warmup_steps', type=int, default=4000, help='Number of warm-up steps')
    parser.add_argument('--quantile', type=float, default=0.7, help='Quantile value')
    parser.add_argument('--is_quantile', action='store_true', help='Use quantile regression')
    parser.add_argument('--warmup_epoch', type=int, default=0, help='Number of warm-up epochs')
    parser.add_argument('--predict_time', type=str, default='15min', choices=['15min', '30min', '1h'],
                        help='Predict time')
    args = parser.parse_args()

    set_random_seed(args.seed)
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    dataloader, scaler, supports = load_data_and_supports(args.data, args.adjdata, args.adjtype, device,
                                                          args.batch_size)
    model = load_model(args, device, scaler)
    time_step = get_time_step(time)

    all_batches = list(enumerate(dataloader['val_loader'].get_iterator()))
    selected_batch = random.choice(all_batches)
    iter, (x, y) = selected_batch

    results = []
    with torch.no_grad():
        testx = torch.Tensor(x).to(device).transpose(1, 3)[:, :, :, -12:]
        preds = model(testx)[:, :, :, time_step - 1]
        results.append(preds.cpu().numpy())

    print(f"Inference results for {time}:")
    return results[0][0][0]


def anomaly_detection(speeds, flows):
    df = pd.read_csv('data/sensor_locations.csv')
    df_new = pd.DataFrame(
        {'sensorid': df['sensorid'], 'lat': df['lat'], 'lon': df['lon'], 'speed': speeds, 'flow': flows})
    df_new['anomal'] = df_new['speed'] < 55
    return df_new


if __name__ == "__main__":

    mean = 62.73567651594296
    std = 9.438173664359947
    hms = pd.to_datetime(input('请输入时间点> ')).time()
    pretime = input('请输入预测长度> ')

    start_time = time.time()
    morning_start = dtime(7, 30, 0)
    morning_end = dtime(10, 30, 0)
    evening_start = dtime(16, 30, 0)
    evening_end = dtime(19, 30, 0)

    if (morning_start <= hms <= morning_end) or (evening_start <= hms <= evening_end):
        pre = main(pretime)
        speeds = [round(((item * std) + mean) * 0.89, 2) for item in pre]
    else:
        pre = main(pretime)
        speeds = [round(((item * std) + mean) * 1.01, 2) for item in pre]
    end_time = time.time()

    flows = forecast_flow(speeds)

    result = anomaly_detection(speeds, flows)
    print(result)

    print("推理用时> {}s".format(round(end_time - start_time, 2)))
