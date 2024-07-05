import pandas as pd
import numpy as np

start_time = '2024-01-01 00:00:00'
end_time = '2024-06-30 23:55:00'
time_points = pd.date_range(start=start_time, end=end_time, freq='5min')

scol = pd.read_csv('../speed_data.csv') # 使用旧文件获取所有传感器id
sensor = scol.keys().tolist()[1:]

data = np.load('PEMSBAY_2024.npy')
data = data[:, :, 1:2]
speed_data = data.reshape(52416, 325, 1)

df = pd.DataFrame(index=time_points, columns=sensor)
for i in range(len(time_points)):
    print("轮次>", i)
    for j in range(len(sensor)):
        df.loc[time_points[i], sensor[j]] = speed_data[i][j][0]
print(df)

df.to_csv('speed_data.csv', index_label='time')
