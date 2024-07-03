import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json


def max_top_sensors(timestep, n):
    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    top_sensors = row_data.nlargest(n)

    top = top_sensors.max() + 0.5
    if top_sensors.min() == 0:
        bottom = 0
    else:
        bottom = top_sensors.min() - 1

    plt.figure(figsize=(10, 6))
    bar_plot = plt.bar(top_sensors.index, top_sensors.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
    plt.xlabel('Sensor ID')
    plt.ylabel('Speed Value')
    plt.title('Top {} Sensor Speeds at {}'.format(n, timestep))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(np.arange(bottom, top, 1), fontsize=10)
    plt.ylim(bottom, top)

    for i, v in enumerate(top_sensors):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=10)

    plt.bar_label(bar_plot, labels=top_sensors.values, label_type='edge', fontsize=10)

    plt.tight_layout()
    plt.show()


def max_top_street(timestep, n):
    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_speed = round(selected_data.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)

    top = top_street.max() + 0.5
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(top_street.index, top_street.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
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
    plt.show()


def avg_top_sensors(start_time, end_time, n):
    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    top_sensors = avg_speeds.nlargest(n)

    top = top_sensors.max() + 0.5
    if top_sensors.min() == 0:
        bottom = 0
    else:
        bottom = top_sensors.min() - 1

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
    plt.show()


def avg_top_street(start_time, end_time, n):
    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    file_path = 'speed_data.csv'
    data = pd.read_csv(file_path)
    data.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_speed = round(temp.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)

    top = top_street.max() + 0.5
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(top_street.index, top_street.values, color='skyblue', width=0.8, edgecolor='black',
                       linewidth=1)
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
    plt.show()


def plot_sensor_speed(sensorid, start_time, end_time):
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
    plt.show()


def plot_street_speed(street, start_time, end_time):
    file = 'sensor_street.json'
    with open(file, 'r') as f:
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
    plt.show()


if __name__ == '__main__':
    # max_top_street('2017-01-01 00:00:00', 5)
    plot_street_speed('Bayshore Freeway', '2017-05-01 00:00:00', '2017-05-08 00:00:00')
    # avg_top_street('2017-05-01 00:00:00', '2017-05-02 00:00:00', 10)
