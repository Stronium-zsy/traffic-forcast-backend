# Traffic-Forecast 项目后端

后端主要实现数据存储，数据分析，模型预测，异常检测等功能

## 文件结构说明

### data analysis

此文件夹用于数据分析

- utils.py：工具文件，提供根据前端传入的数据生成传感器级别和街道级别的数据分析图表。
- sensor_street.json：记录传感器在各街道的分布情况。
- speed_data.txt：数据文件，请根据里面的链接自行下载。

### data visualization

此文件夹用于将传感器在地图上的可视化

- graph_sensor_locations_bay.csv：保存传感器的经纬度坐标。
- trans_data.py：绘制地图脚本（需要下载pems-bay.h5文件）。
- map.html：可视化地图文件。

### database

此文件夹用于数据库的搭建

- sql.md：数据库表的创建方法。
- data_to_db.py：将pems-bay.h5文件写入数据库的脚本。

### make_dateset
此文件夹用于创建项目的数据集

### model

此文件夹用于本项目的模型管理和推理，包含用于加载和应用交通预测模型的脚本和文件。
<br> 关于TESTAM模型的细节，请参考原论文链接： https://github.com/HyunWookL/TESTAM

- local_inference.py：加载预训练模型进行本地推理，并对预测结果做异常检测。
- model_pth：保存训练好的模型文件。
