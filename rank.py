import json


def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def sort_sensor_data_by_count(sensor_data):
    # 按照传感器ID列表的长度进行降序排序
    sorted_data = dict(sorted(sensor_data.items(), key=lambda item: len(item[1]), reverse=True))
    return sorted_data


if __name__ == "__main__":
    input_file = 'sensor_data.json'  # 输入的 JSON 文件路径
    output_file = 'sorted_sensor_street.json'  # 输出的排序后的 JSON 文件路径

    # 读取 JSON 文件中的数据
    sensor_data = read_sensor_data(input_file)

    # 对数据进行排序
    sorted_sensor_data = sort_sensor_data_by_count(sensor_data)

    # 将排序后的数据保存为 JSON 文件
    save_as_json(sorted_sensor_data, output_file)

    print(f"Data successfully sorted and saved to {output_file}")
