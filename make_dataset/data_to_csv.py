import pandas as pd
import numpy as np

start_time = '2024-01-01 00:00:00'
end_time = '2024-06-30 23:55:00'
time_points = pd.date_range(start=start_time, end=end_time, freq='5min')

scol = pd.read_csv('sensor_locations.csv')
sensor = scol['sensorid']

data = np.load('PEMSBAY_2024.npy')
fdata = data[:, :, 0]
sdata = data[:, :, 1]
flow_data = fdata.reshape(52416, 325, 1)
speed_data = sdata.reshape(52416, 325, 1)

df = pd.DataFrame(index=time_points, columns=sensor)
for i in range(len(time_points)):
    print("轮次>", i)
    for j in range(len(sensor)):
        df.loc[time_points[i], sensor[j]] = flow_data[i][j][0]
df = df.rename(columns={'sensorid': 'time'})

# df.to_csv('flow_data.csv', index_label='time')
