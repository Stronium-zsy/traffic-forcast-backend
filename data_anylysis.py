from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import io

app = Flask(__name__)
CORS(app)

def add_seconds_to_time(time_str):
    # Ensure the time string ends with ":00" for seconds
    if len(time_str) == 16:
        return time_str + ":00"
    return time_str

@app.route('/max_top_sensors', methods=['GET'])
def max_top_sensors_route():
    timestep = add_seconds_to_time(request.args.get('timestep'))
    n = int(request.args.get('n'))

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    top_sensors = row_data.nlargest(n)

    top = top_sensors.max() + 0.5
    bottom = 0 if top_sensors.min() == 0 else top_sensors.min() - 1

    plt.figure(figsize=(10, 6))
    bar_plot = plt.bar(top_sensors.index, top_sensors.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Sensor ID')
    plt.ylabel('Speed Value')
    plt.title('Top {} Sensor Speeds at {}'.format(n, timestep))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)
    plt.bar_label(bar_plot, labels=top_sensors.values, label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/min_bottom_sensors', methods=['GET'])
def min_bottom_sensors_route():
    timestep = add_seconds_to_time(request.args.get('timestep'))
    n = int(request.args.get('n'))

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    bottom_sensors = row_data.nsmallest(n)

    top = bottom_sensors.max() + 0.5
    bottom = 0 if bottom_sensors.min() == 0 else bottom_sensors.min() - 1

    plt.figure(figsize=(10, 6))
    bar_plot = plt.bar(bottom_sensors.index, bottom_sensors.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Sensor ID')
    plt.ylabel('Speed Value')
    plt.title('Bottom {} Sensor Speeds at {}'.format(n, timestep))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)
    plt.bar_label(bar_plot, labels=bottom_sensors.values, label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/max_top_street', methods=['GET'])
def max_top_street_route():
    timestep = add_seconds_to_time(request.args.get('timestep'))
    n = int(request.args.get('n'))

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series(dtype=float)
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_speed = round(selected_data.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)

    top = top_street.max() + 0.5
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(top_street.index, top_street.values, color='skyblue', width=0.8, edgecolor='black', linewidth=1)
    plt.xlabel('Street')
    plt.ylabel('Speed Value')
    plt.title('Top {} Street Speeds at {}'.format(n, timestep))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(top_street.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in top_street.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/min_bottom_street', methods=['GET'])
def min_bottom_street_route():
    timestep = add_seconds_to_time(request.args.get('timestep'))
    n = int(request.args.get('n'))

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series(dtype=float)
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_speed = round(selected_data.mean(), 2)
        street_speed[street] = avg_speed
    bottom_street = street_speed.nsmallest(n)

    top = bottom_street.max() + 0.5
    bottom = bottom_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(bottom_street.index, bottom_street.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Street')
    plt.ylabel('Speed Value')
    plt.title('Bottom {} Street Speeds at {}'.format(n, timestep))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(bottom_street.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in bottom_street.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_sensors', methods=['GET'])
def avg_top_sensors_route():
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))
    n = int(request.args.get('n'))

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    top_sensors = avg_speeds.nlargest(n)

    top = top_sensors.max() + 0.5
    bottom = 0 if top_sensors.min() == 0 else top_sensors.min() - 1

    plt.figure(figsize=(10, 6))
    bar_plot = plt.bar(top_sensors.index, top_sensors.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Sensor ID')
    plt.ylabel('Average Speed Value')
    plt.title('Top {} Sensor Average Speeds from {} to {}'.format(n, start_time, end_time))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(top_sensors.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in top_sensors.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_sensors', methods=['GET'])
def avg_bottom_sensors_route():
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))
    n = int(request.args.get('n'))

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    bottom_sensors = avg_speeds.nsmallest(n)

    top = bottom_sensors.max() + 0.5
    bottom = 0 if bottom_sensors.min() == 0 else bottom_sensors.min() - 1

    plt.figure(figsize=(10, 6))
    bar_plot = plt.bar(bottom_sensors.index, bottom_sensors.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Sensor ID')
    plt.ylabel('Average Speed Value')
    plt.title('Bottom {} Sensor Average Speeds from {} to {}'.format(n, start_time, end_time))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(bottom_sensors.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in bottom_sensors.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_street', methods=['GET'])
def avg_top_street_route():
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))
    n = int(request.args.get('n'))

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series(dtype=float)
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_speed = round(temp.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)

    top = top_street.max() + 0.5
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(top_street.index, top_street.values, color='skyblue', width=0.8, edgecolor='black', linewidth=1)
    plt.xlabel('Street')
    plt.ylabel('Average Speed Value')
    plt.title('Top {} Street Average Speeds from {} to {}'.format(n, start_time, end_time))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(top_street.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in top_street.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_street', methods=['GET'])
def avg_bottom_street_route():
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))
    n = int(request.args.get('n'))

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series(dtype=float)
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_speed = round(temp.mean(), 2)
        street_speed[street] = avg_speed
    bottom_street = street_speed.nsmallest(n)

    top = bottom_street.max() + 0.5
    bottom = bottom_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(bottom_street.index, bottom_street.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Street')
    plt.ylabel('Average Speed Value')
    plt.title('Bottom {} Street Average Speeds from {} to {}'.format(n, start_time, end_time))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(bottom_street.values):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=["{:.2f}".format(v) for v in bottom_street.values], label_type='edge', fontsize=10)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/plot_sensor_speed', methods=['GET'])
def plot_sensor_speed_route():
    sensorid = request.args.get('sensorid')
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time, sensorid]

    plt.figure(figsize=(12, 6))
    plt.plot(selected_data.values, '-', color='blue', linewidth=1)
    plt.xlabel('Time', fontsize=12)
    x_ticks = np.arange(0, len(selected_data), 12)
    plt.xticks(x_ticks, fontsize=10)
    plt.ylabel('Speed', fontsize=12)
    plt.title('Speed data for sensor {} from {} to {}'.format(sensorid, start_time, end_time), fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/plot_street_speed', methods=['GET'])
def plot_street_speed_route():
    street = request.args.get('street')
    start_time = add_seconds_to_time(request.args.get('start_time'))
    end_time = add_seconds_to_time(request.args.get('end_time'))

    with open('sensor_street.json', 'r') as f:
        data = json.load(f)
    sensor_list = data[street]

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time, sensor_list]

    average_speed = selected_data.mean(axis=1)

    plt.figure(figsize=(12, 6))
    plt.plot(average_speed.values, '-', color='blue', linewidth=1)
    plt.xlabel('Time', fontsize=12)
    x_ticks = np.arange(0, len(average_speed), 12)
    plt.xticks(x_ticks, fontsize=10)
    plt.ylabel('Speed', fontsize=12)
    plt.title('Speed data for {} from {} to {}'.format(street, start_time, end_time), fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
