import requests

def get_address_by_lat_lon(api_key, lat, lon, level):

    # 构建请求URL
    url = f'https://api.slpy.com/v1/search?level={level}&lat={lat}&lon={lon}&key={api_key}'

    # 设置请求头（如果需要）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    try:
        # 发起请求
        response = requests.get(url, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应的JSON数据
            data = response.json()

            # 打印或处理数据
            print(data)
        elif response.status_code == 403:
            print('Error 403: Forbidden. The request was refused by the server.')
        else:
            print(f'Error: {response.status_code}')

    except requests.RequestException as e:
        print(f'Error: {e}')

# 示例 API key 和经纬度
api_key = '0cf99bf49aa2cef9f56d44441'
latitude = 37.7749
longitude = -122.4194
level = 7  # 示例位置层级，可以根据API文档调整

# 获取地址信息
get_address_by_lat_lon(api_key, latitude, longitude, level)
