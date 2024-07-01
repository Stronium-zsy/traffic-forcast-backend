import h5py
import pandas as pd
import folium
import webbrowser

file = 'C:/Users/27135/Desktop/Urban computing/dataset/pems-bay.h5'

f = h5py.File(file, 'r')

f.keys()
print(f['speed'].keys())  # 项
print(f['speed']['axis0'][:].shape, f['speed']['axis0'][:])  # 传感器id
datetimes = pd.to_datetime(f['speed']['axis1'][:])  # 观测时间
print(datetimes)
print(f['speed']['block0_values'][:].shape, f['speed']['block0_values'][:])  # 每时间每传感器速度

df = pd.read_csv("C:/Users/27135/Desktop/Urban computing/dataset/graph_sensor_locations_bay.csv",
                 names=['station_id', 'lat', 'lon'])
mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=12)
for i in df.iterrows():
    tmp_lat = i[1]['lat']
    tmp_lon = i[1]['lon']
    tmp_id = i[1]['station_id']
    folium.Marker(location=(tmp_lat, tmp_lon),
                  popup=str(int(tmp_id)) + ' : ' + str(tmp_lat) + ' , ' + str(tmp_lon)).add_to(m)
# m.save('map.html')
webbrowser.open('map.html')  # 可视化地图
