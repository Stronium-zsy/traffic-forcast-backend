import pandas as pd
import h5py
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# 读取数据
file_path = 'pems-bay.h5'
with h5py.File(file_path, 'r') as f:
    datetimes = pd.to_datetime(f['speed']['axis1'][:])
    speed_data = f['speed']['block0_values'][:]

# 创建DataFrame
data_dict = {'timestep': datetimes}
for i in range(speed_data.shape[1]):
    data_dict[f'sensor{i + 1}'] = speed_data[:, i]

traffic_data = pd.DataFrame(data_dict)

# 设置数据库连接
user = 'username'
password = 'password'
host = '127.0.0.1'
port = '3306'
database = 'transinfo'

# 创建数据库引擎
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# 插入数据到数据库
try:
    with engine.begin() as connection:
        traffic_data.to_sql('traffic_data', con=connection, if_exists='append', index=False, chunksize=1000)
    print("Data has been successfully inserted into the database.")
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")
    print("Rolling back the transaction.")
