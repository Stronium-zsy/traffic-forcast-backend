# Traffic-Forecast 项目后端

后端主要实现数据存储、数据分析、模型训练与评估、模型本地部署推理以及异常检测等功能。

## 文件结构说明

### data_analysis

该文件夹用于数据分析

- utils.py：工具文件，根据前端传入的数据生成多种传感器级别和街道级别的数据分析图表。
- sensor_street.json：记录传感器在各街道的分布情况。
- speed_data.csv：请运行 make_dataset 文件夹中的 data_to_csv.py 脚本以生成 speed_data.csv 文件。
- flow_data.csv：请运行 make_dataset 文件夹中的 data_to_csv.py 脚本以生成 flow_data.csv 文件。

### database

该文件夹用于数据库的搭建

- sql.md：数据库表的创建方法。
- data_to_db.py：将pems-bay.h5文件写入数据库的脚本。


### make_dateset

该文件夹用于创建项目的数据集。
<br>我们采集了2024年1月1日00:00:00至2024年6月30日23:55:00期间位于美国加利福尼亚州湾区的325个重要传感器所记录的交通数据。数据每隔5分钟记录一次，其中包括速度和车流量这两个重要特征。

- PEMSBAY_2024.npy.txt：原始数据文件，请通过提供的链接自行下载。
- make_dataset.py：该脚本用于构建用于模型训练和评估的数据集，其格式与经典的PEMS2017数据集一致。
- data_to_csv.py：该脚本用于生成用于数据分析的 speed_data.csv 文件和 flow_data.csv 文件。

### model

该文件夹用于管理和推理本项目的模型，包含用于加载和应用交通预测模型的脚本和文件。
<br> 关于TESTAM模型的详细信息，请参考原论文链接： https://github.com/HyunWookL/TESTAM

- data/PEMS-BAY：请运行make_dataset文件夹中的make_dataset.py脚本，以生成模型的数据集并将其保存到此目录下。
- local_inference.py：该脚本加载预训练模型进行本地推理，输出速度和车流量的预测结果，并对结果进行异常检测。
- model_pth：该文件夹保存训练好的模型参数文件。

### myLLM.py

该脚本通过调用阿里云API对通义千问大模型进行访问，通过RAG技术和提示词工程以适应交通项目的应用场景。
