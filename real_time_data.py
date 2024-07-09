import requests

# 替换为您的API密钥
api_key = "G0AWEbbGGRON8I0sytEYQkRZRr1npJvT"
# 替换为您要查询的经纬度和缩放级别
latitude = 52.3676
longitude = 4.9041
zoom = 10

# 构造请求URL
url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point=52.41072,4.84239"

# 发送GET请求
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    # 解析JSON响应
    data = response.json()
    # 打印交通流量信息
    print("交通流量信息:")
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if 'flowSegmentData' in data:
        flow_data = data['flowSegmentData']
        current_speed = flow_data.get('currentSpeed', 'N/A')
        free_flow_speed = flow_data.get('freeFlowSpeed', 'N/A')
        traffic_density = flow_data.get('confidence', 'N/A')
        print(f"当前速度: {current_speed} km/h")
        print(f"自由流动速度: {free_flow_speed} km/h")
        print(f"交通密度: {traffic_density}")
    else:
        print("未找到交通流量数据")
else:
    print(f"请求失败，状态码: {response.status_code}")
