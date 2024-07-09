# Traffic-Forecast 项目后端

后端主要实现数据存储，数据分析，模型预测，异常检测等功能

## 文件结构说明

### data_analysis

此文件夹用于数据分析

- utils.py：工具文件，提供根据前端传入的数据生成传感器级别和街道级别的数据分析图表。
- sensor_street.json：记录传感器在各街道的分布情况。
- speed_data.csv：请运行 make_dataset 文件夹中的 data_to_csv.py 脚本以生成 speed_data.csv 文件。
- flow_data.csv：请运行 make_dataset 文件夹中的 data_to_csv.py 脚本以生成 flow_data.csv 文件。

### database

此文件夹用于数据库的搭建

- sql.md：数据库表的创建方法。
- data_to_db.py：将pems-bay.h5文件写入数据库的脚本。


### make_dateset

此文件夹用于创建项目的数据集
<br>我们收集了2024年1月1日至2024年6月30日期间，每隔5分钟记录的加州湾区325个传感器的交通速度数据。

- PEMSBAY_2024.npy.txt：原始数据文件，请通过提供的链接自行下载。。
- make_dataset.py：构建用于模型训练和评估的数据集，其格式与经典的PEMS2017数据集一致。
- data_to_csv.py：生成用于数据分析的 speed_data.csv 文件和 flow_data.csv 文件。

### model

此文件夹用于本项目的模型管理和推理，包含用于加载和应用交通预测模型的脚本和文件。
<br> 关于TESTAM模型的细节，请参考原论文链接： https://github.com/HyunWookL/TESTAM

- data/PEMS-BAY：请运行 make_dataset 文件夹中的 make_dataset.py 脚本以生成模型的数据集并保存到此目录下。
- local_inference.py：加载预训练模型进行本地推理，并对预测结果做异常检测。
- model_pth：保存训练好的模型文件。
