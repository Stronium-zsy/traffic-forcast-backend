import json


def read_sensor_data(file_path):
    sensor_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                street_name, sensors = line.split(':')
                sensor_ids = [int(float(sid.strip())) for sid in sensors.split(',')]
                sensor_data[street_name.strip()] = sensor_ids
    return sensor_data


def save_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    input_file = 'C:\\Users\\86133\\Documents\\WeChat Files\\wxid_9xkfenvtiujd22\\FileStorage\\File\\2024-07\\sensor_street.txt'  # 输入的文本文件路径
    output_file = 'sensor_data.json'  # 输出的JSON文件路径

    sensor_data = read_sensor_data(input_file)
    save_as_json(sensor_data, output_file)

    print(f"Data successfully saved to {output_file}")
