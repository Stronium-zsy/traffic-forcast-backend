import asyncio
import json
import h5py
import pandas as pd
import websockets

# 加载数据
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

async def send_data(websocket, path):
    time_step = 0
    total_steps = len(datetimes)

    while True:
        num_sensors = len(sensor_ids)
        sensor_data = []
        for s in range(num_sensors):
            speed = float(speed_data[time_step, s])
            sensor_id = int(sensor_ids[s])
            average_speeds[sensor_id]['totalSpeed'] += speed
            average_speeds[sensor_id]['count'] += 1
            sensor_data.append({
                'sensor_id': sensor_id,
                'speed': speed,
                'timestamp': str(datetimes[time_step])
            })

        street_averages = {}
        for street, sensors in street_data.items():
            speeds = [speed_data[time_step, list(sensor_ids).index(sensor_id)] for sensor_id in sensors if
                      sensor_id in sensor_ids]
            if speeds:
                street_averages[street] = sum(speeds) / len(speeds)
            else:
                street_averages[street] = None

        # 对 street_averages 进行排序，并取速度前十的街道
        sorted_street_averages = sorted(street_averages.items(),
                                        key=lambda x: x[1] if x[1] is not None else -float('inf'), reverse=True)[:10]

        # 将排序后的结果转换为字典
        sorted_street_averages = dict(sorted_street_averages)

        # 计算所有传感器的平均速度
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




