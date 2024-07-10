import io
from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json

app = Flask(__name__)
CORS(app)


# ******************************************<传感器级别车速，车流量统计>******************************************
@app.route('/top_speed_sensors', method=['GET'])
def top_speed_sensors():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    top_sensors = row_data.nlargest(n)
    top_sensors = top_sensors[::-1]

    top = top_sensors.max() + 0.5
    bottom = top_sensors.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Greens(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(top_sensors.index, top_sensors.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Sensor ID', fontsize=18, fontweight='bold')
    plt.xlabel('Speed Value', fontsize=18, fontweight='bold')
    plt.title('Top {} Sensor Speeds at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, 1), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 0.25, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/top_flow_sensors', method=['GET'])
def top_flow_sensors():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    top_sensors = row_data.nlargest(n)
    top_sensors = top_sensors[::-1]

    top = top_sensors.max() + 1
    bottom = top_sensors.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Reds(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(top_sensors.index, top_sensors.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Sensor ID', fontsize=18, fontweight='bold')
    plt.xlabel('Flow Value', fontsize=18, fontweight='bold')
    plt.title('Top {} Sensor Flows at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, (top - bottom) / 10), fontsize=14)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/bottom_speed_sensors', method=['GET'])
def bottom_speed_sensors():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    row_data = row_data[row_data != 0]
    bottom_sensors = row_data.nsmallest(n)

    top = bottom_sensors.max() + 0.5
    bottom = bottom_sensors.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Blues(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(bottom_sensors.index, bottom_sensors.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Sensor ID', fontsize=18, fontweight='bold')
    plt.xlabel('Speed Value', fontsize=18, fontweight='bold')
    plt.title('Bottom {} Sensor Speeds at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, 1), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 0.25, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/bottom_flow_sensors', method=['GET'])
def bottom_flow_sensors():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    row_data = data.loc[timestep]
    row_data = row_data[row_data != 0]
    bottom_sensors = row_data.nsmallest(n)

    top = bottom_sensors.max() + 1
    bottom = bottom_sensors.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Oranges(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(bottom_sensors.index, bottom_sensors.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Sensor ID', fontsize=18, fontweight='bold')
    plt.xlabel('Flow Value', fontsize=18, fontweight='bold')
    plt.title('Bottom {} Sensor Flows at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, (top - bottom) / 10), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_speed_sensors', method=['GET'])
def avg_top_speed_sensors():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    top_sensors = avg_speeds.nlargest(n)

    categories = top_sensors.index.tolist()
    values = top_sensors.values.tolist()

    cmap = plt.get_cmap('plasma')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Sensors', fontsize=14, weight='bold')
    ax.set_ylabel('Average Speed', fontsize=14, weight='bold')
    ax.set_title(f'Top {n} Sensor Average Speed from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_flow_sensors', method=['GET'])
def avg_top_flow_sensors():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_flows = round(selected_data.mean())
    top_sensors = avg_flows.nlargest(n)

    categories = top_sensors.index.tolist()
    values = top_sensors.values.tolist()

    cmap = plt.get_cmap('plasma')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Sensors', fontsize=14, weight='bold')
    ax.set_ylabel('Average Flow', fontsize=14, weight='bold')
    ax.set_title(f'Top {n} Sensor Average Flow from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_speed_sensors', method=['GET'])
def avg_bottom_speed_sensors():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    avg_speeds = avg_speeds[avg_speeds != 0]
    bottom_streets = avg_speeds.nsmallest(n)

    categories = bottom_streets.index.tolist()
    values = bottom_streets.values.tolist()

    cmap = plt.get_cmap('inferno')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Sensors', fontsize=14, weight='bold')
    ax.set_ylabel('Average Speed', fontsize=14, weight='bold')
    ax.set_title(f'Bottom {n} Sensor Average Speed from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_flow_sensors', method=['GET'])
def avg_bottom_flow_sensors():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_flows = selected_data.mean()
    avg_flows = avg_flows[avg_flows != 0]
    avg_flows = round(avg_flows)
    bottom_streets = avg_flows.nsmallest(n)

    categories = bottom_streets.index.tolist()
    values = bottom_streets.values.tolist()

    cmap = plt.get_cmap('inferno')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Sensors', fontsize=14, weight='bold')
    ax.set_ylabel('Average Flow', fontsize=14, weight='bold')
    ax.set_title(f'Bottom {n} Sensor Average Flow from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


# ******************************************<街道级别车速，车流量统计>******************************************
@app.route('/top_speed_street', method=['GET'])
def top_speed_street():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_speed = round(selected_data.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)
    top_street = top_street[::-1]

    top = top_street.max() + 0.5
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Greens(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(top_street.index, top_street.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Street', fontsize=18, fontweight='bold')
    plt.xlabel('Speed Value', fontsize=18, fontweight='bold')
    plt.title('Top {} Street Speeds at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, 1), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 0.25, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/top_flow_street', method=['GET'])
def top_flow_street():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    street_flow = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_flow = round(selected_data.mean())
        street_flow[street] = avg_flow
    top_street = street_flow.nlargest(n)
    top_street = top_street[::-1]

    top = top_street.max() + 1
    bottom = top_street.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Reds(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(top_street.index, top_street.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Street', fontsize=18, fontweight='bold')
    plt.xlabel('Flow Value', fontsize=18, fontweight='bold')
    plt.title('Top {} Sensor Flows at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, (top - bottom) / 10), fontsize=14)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/bottom_speed_street', method=['GET'])
def bottom_speed_street():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_speed = round(selected_data.mean(), 2)
        street_speed[street] = avg_speed
    street_speed = street_speed[street_speed != 0]
    bottom_street = street_speed.nsmallest(n)

    top = bottom_street.max() + 0.5
    bottom = bottom_street.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Blues(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(bottom_street.index, bottom_street.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Street', fontsize=18, fontweight='bold')
    plt.xlabel('Speed Value', fontsize=18, fontweight='bold')
    plt.title('Bottom {} Street Speeds at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, 1), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 0.25, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/bottom_flow_street', method=['GET'])
def bottom_flow_street():
    timestep = request.args.get('timestep')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    street_flow = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[timestep, sensor_list]
        avg_flow = round(selected_data.mean())
        street_flow[street] = avg_flow
    street_flow = street_flow[street_flow != 0]
    bottom_street = street_flow.nsmallest(n)

    top = bottom_street.max() + 1
    bottom = bottom_street.min() - 1

    plt.figure(figsize=(12, 8))
    colors = plt.cm.Oranges(np.linspace(0.3, 1, n))
    bar_plot = plt.barh(bottom_street.index, bottom_street.values, color=colors, edgecolor='black', linewidth=1)
    plt.ylabel('Street', fontsize=18, fontweight='bold')
    plt.xlabel('Flow Value', fontsize=18, fontweight='bold')
    plt.title('Bottom {} Street Flows at {}'.format(n, timestep), fontsize=16, fontweight='bold')
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(np.arange(bottom, top, (top - bottom) / 10), fontsize=15)
    plt.xlim(bottom, top)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    for bar in bar_plot:
        plt.gca().text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                       f'{bar.get_width():.2f}', ha='center', va='center', fontsize=13, color='black',
                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.6))

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_speed_street', method=['GET'])
def avg_top_speed_street():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_speed = round(temp.mean(), 2)
        street_speed[street] = avg_speed
    top_street = street_speed.nlargest(n)

    categories = top_street.index.tolist()
    values = top_street.values.tolist()

    cmap = plt.get_cmap('plasma')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Streets', fontsize=14, weight='bold')
    ax.set_ylabel('Average Speed', fontsize=14, weight='bold')
    ax.set_title(f'Top {n} Streets Average Speed from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_top_flow_street', method=['GET'])
def avg_top_flow_street():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    street_flow = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_flow = round(temp.mean())
        street_flow[street] = avg_flow
    top_street = street_flow.nlargest(n)

    categories = top_street.index.tolist()
    values = top_street.values.tolist()

    cmap = plt.get_cmap('plasma')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Streets', fontsize=14, weight='bold')
    ax.set_ylabel('Average Flow', fontsize=14, weight='bold')
    ax.set_title(f'Top {n} Streets Average Flow from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_speed_street', method=['GET'])
def avg_bottom_speed_street():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    street_speed = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_speed = round(temp.mean(), 2)
        street_speed[street] = avg_speed
    street_speed = street_speed[street_speed != 0]
    bottom_street = street_speed.nsmallest(n)

    categories = bottom_street.index.tolist()
    values = bottom_street.values.tolist()

    cmap = plt.get_cmap('inferno')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Street', fontsize=14, weight='bold')
    ax.set_ylabel('Average Speed', fontsize=14, weight='bold')
    ax.set_title(f'Bottom {n} Street Average Speed from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/avg_bottom_flow_street', method=['GET'])
def avg_bottom_flow_street():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    n = request.args.get('n')

    with open('sensor_street.json', 'r') as f:
        json_data = json.load(f)

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    street_flow = pd.Series()
    for street, sensor_list in json_data.items():
        selected_data = data.loc[start_time:end_time, sensor_list]
        temp = selected_data.mean(axis=1)
        avg_flow = round(temp.mean())
        street_flow[street] = avg_flow
    street_flow = street_flow[street_flow != 0]
    bottom_street = street_flow.nsmallest(n)

    categories = bottom_street.index.tolist()
    values = bottom_street.values.tolist()

    cmap = plt.get_cmap('inferno')
    colors = [cmap(i / n) for i in range(n)]

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='grey')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom', ha='center', fontsize=12,
                weight='bold', color='black')
    ax.set_xlabel('Street', fontsize=14, weight='bold')
    ax.set_ylabel('Average Flow', fontsize=14, weight='bold')
    ax.set_title(f'Bottom {n} Street Average Flow from {start_time} to {end_time}', fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


# ******************************************<车速，车流量分布统计>******************************************
@app.route('/speed_distribution', method=['GET'])
def speed_distribution():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()

    bins = [0, 50, 60, 62.5, 65, 67.5, float('inf')]
    labels = ['<50', '50-60', '60-62.5', '62.5-65', '65-67.5', '>67.5']
    speed_categories = pd.cut(avg_speeds, bins=bins, labels=labels, right=False)
    speed_distribution = speed_categories.value_counts()

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0.15, 0.75, len(speed_distribution)))
    wedges, texts, autotexts = ax.pie(
        speed_distribution.values,
        labels=speed_distribution.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=0.5)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, speed_distribution.index,
              title="Speed Range",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='10')

    plt.title('Speed Distribution from {} to {}'.format(start_time, end_time), fontsize=14, weight='bold')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/flow_distribution', method=['GET'])
def flow_distribution():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_flows = selected_data.mean()

    bins = [0, 150, 200, 225, 250, 275, float('inf')]
    labels = ['<150', '150-200', '200-225', '225-250', '250-275', '>275']
    speed_categories = pd.cut(avg_flows, bins=bins, labels=labels, right=False)
    speed_distribution = speed_categories.value_counts()

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0.15, 0.75, len(speed_distribution)))
    wedges, texts, autotexts = ax.pie(
        speed_distribution.values,
        labels=speed_distribution.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=0.5)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, speed_distribution.index,
              title="Speed Range",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='10')

    plt.title('Flow Distribution from {} to {}'.format(start_time, end_time), fontsize=14, weight='bold')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


# ******************************************<传感器级别车速，车流量时序统计>******************************************
@app.route('/plot_sensor_speed', method=['GET'])
def plot_sensor_speed():
    sensorid = request.args.get('sensorid')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    data = pd.read_csv('speed_data.csv')
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


@app.route('/plot_sensor_flow', method=['GET'])
def plot_sensor_flow():
    sensorid = request.args.get('sensorid')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time, sensorid]

    plt.figure(figsize=(12, 6))
    plt.plot(selected_data.values, '-', color='blue', linewidth=1)
    plt.xlabel('Time', fontsize=12)
    x_ticks = np.arange(0, len(selected_data), 12)
    plt.xticks(x_ticks, fontsize=10)
    plt.ylabel('Flow', fontsize=12)
    plt.title('Flow data for sensor {} from {} to {}'.format(sensorid, start_time, end_time), fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


# ******************************************<街道级别车速，车流量时序统计>******************************************
@app.route('/plot_street_speed', method=['GET'])
def plot_street_speed():
    street = request.args.get('street')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    with open('sensor_street.json', 'r') as f:
        data = json.load(f)
    sensor_list = data[street]

    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time, sensor_list]

    avg_speed = selected_data.mean(axis=1)

    plt.figure(figsize=(12, 6))
    plt.plot(avg_speed.values, '-', color='blue', linewidth=1)
    plt.xlabel('Time', fontsize=12)
    x_ticks = np.arange(0, len(avg_speed), 12)
    plt.xticks(x_ticks, fontsize=10)
    plt.ylabel('Speed', fontsize=12)
    plt.title('Speed data for {} from {} to {}'.format(street, start_time, end_time), fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.route('/plot_street_flow', method=['GET'])
def plot_street_flow():
    street = request.args.get('street')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    with open('sensor_street.json', 'r') as f:
        data = json.load(f)
    sensor_list = data[street]

    data = pd.read_csv('flow_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time, sensor_list]

    avg_flow = selected_data.mean(axis=1)

    plt.figure(figsize=(12, 6))
    plt.plot(avg_flow.values, '-', color='blue', linewidth=1)
    plt.xlabel('Time', fontsize=12)
    x_ticks = np.arange(0, len(avg_flow), 12)
    plt.xticks(x_ticks, fontsize=10)
    plt.ylabel('Flow', fontsize=12)
    plt.title('Flow data for {} from {} to {}'.format(street, start_time, end_time), fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)

    # top_speed_sensors('2024-03-01 18:00:00', 10)
    # top_flow_sensors('2024-03-01 18:00:00', 10)
    # bottom_speed_sensors('2024-03-01 18:00:00', 10)
    # bottom_flow_sensors('2024-03-01 18:00:00', 10)
    # avg_top_speed_sensors('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_top_flow_sensors('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_bottom_speed_sensors('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_bottom_flow_sensors('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)

    # top_speed_street('2024-05-01 09:30:00', 10)
    # top_flow_street('2024-05-01 09:30:00', 10)
    # bottom_speed_street('2024-05-01 09:30:00', 10)
    # bottom_flow_street('2024-05-01 09:30:00', 10)
    # avg_top_speed_street('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_top_flow_street('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_bottom_speed_street('2024-04-01 00:00:00', '2024-04-02 00:00:00', 10)
    # avg_bottom_flow_street('2024-04-01 00:00:00', '2024-04-02 00:00:00', 10)

    # speed_distribution('2024-04-01 00:00:00', '2024-04-02 00:00:00')
    # flow_distribution('2024-04-01 00:00:00', '2024-04-02 00:00:00')

    # plot_sensor_speed('400236', '2024-05-01 00:00:00', '2024-05-07 00:00:00')
    # plot_sensor_flow('400236', '2024-05-01 00:00:00', '2024-05-07 00:00:00')
    # plot_street_speed('Bayshore Freeway', '2024-05-29 00:00:00', '2024-06-05 00:00:00')
    # plot_street_flow('Bayshore Freeway', '2024-05-29 00:00:00', '2024-06-05 00:00:00')
