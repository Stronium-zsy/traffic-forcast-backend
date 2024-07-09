import heapq
import numpy as np
import h5py
import pandas as pd
import folium
import webbrowser
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转换为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine 公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # 地球平均半径，单位为公里
    r = 6371.0 

    # 计算结果
    distance = c * r
    return distance



def dijkstra(graph, start_vertex, end_vertex):
    shortest_paths = {vertex: float('inf') for vertex in range(325)}
    shortest_paths[start_vertex] = 0
    priority_queue = [(0, start_vertex)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # 如果到达目标节点，提前退出
        if current_vertex == end_vertex:
            return current_distance
        
        if current_distance > shortest_paths[current_vertex]:
            continue
        
        for neighbor in range(325):
            weight = graph[current_vertex][neighbor]
            if weight != float('inf'):  # 确保有边存在
                distance = current_distance + weight
                if distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_paths[end_vertex]


import argparse
import pandas as pd
from datetime import time
import torch
import numpy as np
import util
from engine import trainer
import random


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
    # supports = [torch.tensor(i).to(device) for i in adj_mx]
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

data_map = {
    1: 400001.0,2: 400017.0,3: 400030.0,4: 400040.0,5: 400045.0,6: 400052.0,7: 400057.0,8: 400059.0,9: 400065.0,10: 400069.0,
    11: 400073.0,12: 400084.0,13: 400085.0,14: 400088.0,15: 400096.0,16: 400097.0,17: 400100.0,18: 400104.0,19: 400109.0,20: 400122.0,
    21: 400147.0,22: 400148.0,23: 400149.0,24: 400158.0,25: 400160.0,26: 400168.0,27: 400172.0,28: 400174.0,29: 400178.0,30: 400185.0,
    31: 400201.0,32: 400206.0,33: 400209.0,34: 400213.0,35: 400221.0,36: 400222.0,37: 400227.0,38: 400236.0,39: 400238.0,40: 400240.0,
    41: 400246.0,42: 400253.0,43: 400257.0,44: 400258.0,45: 400268.0,46: 400274.0,47: 400278.0,48: 400280.0,49: 400292.0,50: 400296.0,
    51: 400298.0,52: 400330.0,53: 400336.0,54: 400343.0,55: 400353.0,56: 400372.0,57: 400394.0,58: 400400.0,59: 400414.0,60: 400418.0,
    61: 400429.0,62: 400435.0,63: 400436.0,64: 400440.0,65: 400449.0,66: 400457.0,67: 400461.0,68: 400464.0,69: 400479.0,70: 400485.0,
    71: 400499.0,72: 400507.0,73: 400508.0,74: 400514.0,75: 400519.0,76: 400528.0,77: 400545.0,78: 400560.0,79: 400563.0,80: 400567.0,
    81: 400581.0,82: 400582.0,83: 400586.0,84: 400637.0,85: 400643.0,86: 400648.0,87: 400649.0,88: 400654.0,89: 400664.0,90: 400665.0,
    91: 400668.0,92: 400673.0,93: 400677.0,94: 400687.0,95: 400688.0,96: 400690.0,97: 400700.0,98: 400709.0,99: 400713.0,100: 400714.0,
    101: 400715.0,102: 400717.0,103: 400723.0,104: 400743.0,105: 400750.0,106: 400760.0,107: 400772.0,108: 400790.0,109: 400792.0,110: 400794.0,
    111: 400799.0,112: 400804.0,113: 400822.0,114: 400823.0,115: 400828.0,116: 400832.0,117: 400837.0,118: 400842.0,119: 400863.0,120: 400869.0,
    121: 400873.0,122: 400895.0,123: 400904.0,124: 400907.0,125: 400911.0,126: 400916.0,127: 400922.0,128: 400934.0,129: 400951.0,130: 400952.0,
    131: 400953.0,132: 400964.0,133: 400965.0,134: 400970.0,135: 400971.0,136: 400973.0,137: 400995.0,138: 400996.0,139: 401014.0,140: 401129.0,
    141: 401154.0,142: 401163.0,143: 401167.0,144: 401210.0,145: 401224.0,146: 401327.0,147: 401351.0,148: 401388.0,149: 401391.0,150: 401400.0,
    151: 401403.0,152: 401440.0,153: 401457.0,154: 401464.0,155: 401489.0,156: 401495.0,157: 401507.0,158: 401534.0,159: 401541.0,160: 401555.0,
    161: 401560.0,162: 401567.0,163: 401597.0,164: 401606.0,165: 401611.0,166: 401655.0,167: 401808.0,168: 401809.0,169: 401810.0,170: 401811.0,
    171: 401816.0,172: 401817.0,173: 401845.0,174: 401846.0,175: 401890.0,176: 401891.0,177: 401906.0,178: 401908.0,179: 401926.0,180: 401936.0,
    181: 401937.0,182: 401942.0,183: 401943.0,184: 401948.0,185: 401957.0,186: 401958.0,187: 401994.0,188: 401996.0,189: 401997.0,190: 401998.0,
    191: 402056.0,192: 402057.0,193: 402058.0,194: 402059.0,195: 402060.0,196: 402061.0,197: 402067.0,198: 402117.0,199: 402118.0,200: 402119.0,
    201: 402120.0,202: 402121.0,203: 402281.0,204: 402282.0,205: 402283.0,206: 402284.0,207: 402285.0,208: 402286.0,209: 402287.0,210: 402288.0,
    211: 402289.0,212: 402359.0,213: 402360.0,214: 402361.0,215: 402362.0,216: 402363.0,217: 402364.0,218: 402365.0,219: 402366.0,220: 402367.0,
    221: 402368.0,222: 402369.0,223: 402370.0,224: 402371.0,225: 402372.0,226: 402373.0,227: 403225.0,228: 403265.0,229: 403329.0,230: 403401.0,
    231: 403402.0,232: 403404.0,233: 403406.0,234: 403409.0,235: 403412.0,236: 403414.0,237: 403419.0,238: 404370.0,239: 404434.0,240: 404435.0,
    241: 404444.0,242: 404451.0,243: 404452.0,244: 404453.0,245: 404461.0,246: 404462.0,247: 404521.0,248: 404522.0,249: 404553.0,250: 404554.0,
    251: 404585.0,252: 404586.0,253: 404640.0,254: 404753.0,255: 404759.0,256: 405613.0,257: 405619.0,258: 405701.0,259: 407150.0,260: 407151.0,
    261: 407152.0,262: 407153.0,263: 407155.0,264: 407157.0,265: 407161.0,266: 407165.0,267: 407172.0,268: 407173.0,269: 407174.0,270: 407176.0,
    271: 407177.0,272: 407179.0,273: 407180.0,274: 407181.0,275: 407184.0,276: 407185.0,277: 407186.0,278: 407187.0,279: 407190.0,280: 407191.0,
    281: 407194.0,282: 407200.0,283: 407202.0,284: 407204.0,285: 407206.0,286: 407207.0,287: 407321.0,288: 407323.0,289: 407325.0,290: 407328.0,
    291: 407331.0,292: 407332.0,293: 407335.0,294: 407336.0,295: 407337.0,296: 407339.0,297: 407341.0,298: 407342.0,299: 407344.0,300: 407348.0,
    301: 407352.0,302: 407359.0,303: 407360.0,304: 407361.0,305: 407364.0,306: 407367.0,307: 407370.0,308: 407372.0,309: 407373.0,310: 407374.0,
    311: 407710.0,312: 407711.0,313: 408907.0,314: 408911.0,315: 409524.0,316: 409525.0,317: 409526.0,318: 409528.0,319: 409529.0,320: 413026.0,
    321: 413845.0,322: 413877.0,323: 413878.0,324: 414284.0,325: 414694.0
}

reversed_data_map = {v: k for k, v in data_map.items()}

def main(time):
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda:0', help='Device to use for computation')
    parser.add_argument('--data', type=str, default='./data/PEMS-BAY', help='Data path')
    parser.add_argument('--adjdata', type=str, default='./data/PEMS-BAY/adj_mx.pkl', help='Adjacency data path')
    parser.add_argument('--adjtype', type=str, default='doubletransition', help='Adjacency type')
    parser.add_argument('--seq_length', type=int, default=12, help='Sequence length')
    parser.add_argument('--nhid', type=int, default=32, help='Number of hidden units')
    parser.add_argument('--in_dim', type=int, default=2, help='Input dimension')
    parser.add_argument('--num_nodes', type=int, default=325, help='Number of nodes')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--dropout', type=float, default=0.3, help='Dropout rate')
    parser.add_argument('--seed', type=int, default=99, help='Random seed')
    parser.add_argument('--load_path', type=str,
                        default='E:/training/1/traffic-forcast-backend-main/model/TESTAM/model_pth/BEST_PEMS-BAY_1.19.pth')
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
    dataloader, scaler = load_data_and_supports(args.data, args.adjdata, args.adjtype, device,
                                                          args.batch_size)
    model = load_model(args, device, scaler)
    time_step = get_time_step(time)

    all_batches = list(enumerate(dataloader['val_loader'].get_iterator()))
    selected_batch = random.choice(all_batches)
    iter, (x, y) = selected_batch

    results = []
    with torch.no_grad():
        testx = torch.Tensor(x).to(device).transpose(1, 3)[:, :, :, -24:]
        preds = model(testx)[:, :, :, time_step - 1]
        results.append(preds.cpu().numpy())

    print(f"Inference results for {time}:")
    return results[0][0][0]


if __name__ == "__main__":
    mean = 62.73567651594296
    std = 9.438173664359947
    hms = pd.to_datetime(input('请输入时间点> ')).time()
    pretime = input('请输入预测长度> ')

    morning_start = time(7, 30, 0)
    morning_end = time(10, 0, 0)
    evening_start = time(16, 30, 0)
    evening_end = time(19, 30, 0)

    if (morning_start <= hms <= morning_end) or (evening_start <= hms <= evening_end):
        pre = main(pretime)
        result = [round(((item * std) + mean) * 0.9, 2) for item in pre]
        #print(result)
        
        
    else:
        pre = main(pretime)
        result = [(round((item * std) + mean, 2)) for item in pre]
        #print(result)

    start_node = int(input("请输入开始节点: "))
    end_node = int(input("请输入结束节点: "))
    if start_node in reversed_data_map:
        startnode =reversed_data_map[start_node]
    if end_node in reversed_data_map:
        endnode =reversed_data_map[end_node]
        

    file = 'E:/training/1/traffic-forcast-backend-main/data/pems-bay.h5'

    f = h5py.File(file, 'r')
    
    df = pd.read_csv("E:/training/1/traffic-forcast-backend-main/data visualization/graph_sensor_locations_bay.csv",
                 names=['station_id', 'lat', 'lon'])



    arr = [[0.0] * 325 for _ in range(325)]
    for i in range(325):
        for j in range(325):
            if i == j:
                arr[i][j] = float('inf')
            else:
                arr[i][j] = float(haversine(df.iloc[i, 1], df.iloc[i, 2], df.iloc[j, 1], df.iloc[j, 2]))


    adj_matrix= [[0] *325 for _ in range(325)]
    for i in range(325):
        for j in range(325):
            if i == j:
                adj_matrix[i][j] =float('inf')
            else:
                adj_matrix[i][j] =arr[i][j]/((result[i] + result[j]) / 2)*60
                if arr[i][j]>=8.1:
                    adj_matrix[i][j] =float('inf')


    shortest_distance = dijkstra(adj_matrix, startnode, endnode)
    print(f"The shortest time from node {startnode} to node {endnode} is: {df.iloc[startnode-1, 1], df.iloc[startnode-1, 2], df.iloc[endnode-1, 1], df.iloc[endnode-1, 2]}")
    print(f"The distance from node {startnode} to node {endnode} is: {arr[startnode][endnode]}")
    print(f"The chosen time from node {startnode} to node {endnode} is: {adj_matrix[startnode][endnode]}")
    print(f"The  avg speed from node {startnode} to node {endnode} is: {(result[startnode] + result[endnode]) / 2}")
    print(f"The shortest time from node {startnode} to node {endnode} is: {shortest_distance}")







