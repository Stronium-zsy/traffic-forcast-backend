import json
import requests
import time


def load_initial_markers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        initial_markers = json.load(file)
    return initial_markers


def get_address_by_lat_lon(api_key, lat, lon, level):
    url = f'https://api.slpy.com/v1/search?level={level}&lat={lat}&lon={lon}&key={api_key}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 403:
            print('Error 403: Forbidden. The request was refused by the server.')
        elif response.status_code == 429:
            print('Error 429: Too Many Requests. Retrying after a delay...')
            time.sleep(10)  # 等待10秒钟后重试
            return get_address_by_lat_lon(api_key, lat, lon, level)
        else:
            print(f'Error: {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')
    return None


def get_surrounding_points(lat, lon, distance=0.0003):
    # 生成传感器周围的点
    return [
        (lat + distance, lon),
        (lat - distance, lon),
        (lat, lon + distance),
        (lat, lon - distance),
        (lat + distance / 2, lon + distance / 2),
        (lat - distance / 2, lon - distance / 2),
        (lat + distance / 2, lon - distance / 2),
        (lat - distance / 2, lon + distance / 2)
    ]


def get_streets_for_sensors(api_key, initial_markers, level):
    sensors_with_streets = []
    for sensor in initial_markers:
        sensor_id = sensor['sensor_id']
        lat, lon = sensor['position']
        print(f"Processing sensor {sensor_id} at position ({lat}, {lon})")
        streets = set()

        points = [(lat, lon)] + get_surrounding_points(lat, lon)
        for point in points:
            point_lat, point_lon = point
            address_data = get_address_by_lat_lon(api_key, point_lat, point_lon, level)
            if address_data and 'properties' in address_data and 'street' in address_data['properties']:
                streets.add(address_data['properties']['street'])
                print(
                    f"Found street {address_data['properties']['street']} for sensor {sensor_id} at position ({point_lat}, {point_lon})")
            time.sleep(0.2)  # 添加延迟，降低请求频率

        if streets:
            sensors_with_streets.append({
                'sensor_id': sensor_id,
                'position': [lat, lon],
                'content': sensor['content'],
                'streets': list(streets)
            })
            print(f"Sensor {sensor_id} is located on streets: {list(streets)}")
        else:
            print(f"Failed to get streets for sensor {sensor_id}")

    return sensors_with_streets


def main():
    api_key = '0cf99bf49aa2cef9f56d44441'
    level = 7  # 示例位置层级，可以根据API文档调整

    # 读取 initial_markers 数据
    initial_markers_file_path = 'initial_markers.json'
    initial_markers = load_initial_markers(initial_markers_file_path)

    # 获取每个传感器所在的所有街道
    sensors_with_streets = get_streets_for_sensors(api_key, initial_markers, level)

    # 输出为 JSON 文件
    sensors_with_streets_file_path = 'sensors_with_streets.json'
    with open(sensors_with_streets_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(sensors_with_streets, json_file, ensure_ascii=False, indent=4)
    print(f"Saved sensor data with streets to {sensors_with_streets_file_path}")


if __name__ == "__main__":
    main()
