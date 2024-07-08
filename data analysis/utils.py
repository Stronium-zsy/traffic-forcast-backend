import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json


def max_top_sensors(timestep, n):
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
    plt.show()


def min_bottoom_sensors(timestep, n):
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
    plt.show()


def max_top_street(timestep, n):
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
    plt.show()


def min_bottom_street(timestep, n):
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
    plt.show()


def avg_top_sensors(start_time, end_time, n):
    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    top_sensors = avg_speeds.nlargest(n)

    def autopct_format(pct, allvals):
        absolute = pct / 100.0 * np.sum(allvals)
        return "{:.2f}%\n({:.2f})".format(pct, absolute)

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(top_sensors)))
    wedges, texts, autotexts = ax.pie(
        top_sensors.values,
        labels=top_sensors.index,
        autopct=lambda pct: autopct_format(pct, top_sensors.values),
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=1)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, top_sensors.index,
              title="sensorId",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='12')
    plt.title('Top {} Sensor Average Speeds from {} to {}'.format(n, start_time, end_time), fontsize=14, weight='bold')
    plt.tight_layout()
    plt.show()


def avg_bottom_sensors(start_time, end_time, n):
    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()
    avg_speeds = avg_speeds[avg_speeds != 0]
    bottom_sensors = avg_speeds.nsmallest(n)

    def autopct_format(pct, allvals):
        absolute = pct / 100.0 * np.sum(allvals)
        return "{:.2f}%\n({:.2f})".format(pct, absolute)

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(bottom_sensors)))
    wedges, texts, autotexts = ax.pie(
        bottom_sensors.values,
        labels=bottom_sensors.index,
        autopct=lambda pct: autopct_format(pct, bottom_sensors.values),
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=1)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, bottom_sensors.index,
              title="sensorId",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='12')
    plt.title('Bottom {} Sensor Average Speeds from {} to {}'.format(n, start_time, end_time), fontsize=14,
              weight='bold')
    plt.tight_layout()
    plt.show()


def avg_top_street(start_time, end_time, n):
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

    def autopct_format(pct, allvals):
        absolute = pct / 100.0 * np.sum(allvals)
        return "{:.2f}%\n({:.2f})".format(pct, absolute)

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(top_street)))
    wedges, texts, autotexts = ax.pie(
        top_street.values,
        labels=top_street.index,
        autopct=lambda pct: autopct_format(pct, top_street.values),
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=1)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, top_street.index,
              title="sensorId",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='12')
    plt.title('Top {} Street Average Speeds from {} to {}'.format(n, start_time, end_time), fontsize=14, weight='bold')
    plt.tight_layout()
    plt.show()


def avg_bottom_street(start_time, end_time, n):
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

    def autopct_format(pct, allvals):
        absolute = pct / 100.0 * np.sum(allvals)
        return "{:.2f}%\n({:.2f})".format(pct, absolute)

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(bottom_street)))
    wedges, texts, autotexts = ax.pie(
        bottom_street.values,
        labels=bottom_street.index,
        autopct=lambda pct: autopct_format(pct, bottom_street.values),
        startangle=140,
        colors=colors,
        textprops=dict(color="w"),
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=15, weight="bold")

    def add_gradient_border(ax, wedge, color):
        path = wedge.get_path()
        patch = patches.PathPatch(path, edgecolor=color, facecolor='none', lw=2, alpha=1)
        ax.add_patch(patch)

    for wedge, color in zip(wedges, colors):
        add_gradient_border(ax, wedge, color)

    ax.legend(wedges, bottom_street.index,
              title="sensorId",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize='12')
    plt.title('Bottom {} Street Average Speeds from {} to {}'.format(n, start_time, end_time), fontsize=14,
              weight='bold')
    plt.tight_layout()
    plt.show()


def speed_distribution(start_time, end_time):
    data = pd.read_csv('speed_data.csv')
    data.set_index('time', inplace=True)

    selected_data = data.loc[start_time:end_time]
    avg_speeds = selected_data.mean()

    bins = [0, 50, 60, 62.5, 65, 67.5, float('inf')]
    labels = ['<50', '50-60', '60-62.5', '62.5-65', '65-67.5', '>67.5']
    speed_categories = pd.cut(avg_speeds, bins=bins, labels=labels, right=False)
    speed_distribution = speed_categories.value_counts()

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(speed_distribution)))
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

    plt.title('Sensor Speed Distribution from {} to {}'.format(start_time, end_time), fontsize=14, weight='bold')
    plt.tight_layout()
    plt.show()


def plot_sensor_speed(sensorid, start_time, end_time):
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
    plt.show()


def plot_street_speed(street, start_time, end_time):
    with open('sensor_street.json', 'r') as f:
        data = json.load(f)
    sensor_list = data[street]

    data = pd.read_csv('speed_data.csv')
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
    # max_top_sensors('2024-01-01 12:00:00', 10)
    # min_bottoom_sensors('2024-01-01 12:00:00', 10)
    # max_top_street('2024-05-01 09:30:00', 5)
    # min_bottom_street('2024-05-01 09:30:00', 5)

    # avg_top_sensors('2024-05-01 00:08:00', '2024-05-02 00:18:00', 10)
    # avg_bottom_sensors('2024-05-01 00:00:00', '2024-05-02 00:00:00', 10)
    # avg_top_street('2024-04-01 00:00:00', '2024-04-02 00:00:00', 10)
    # avg_bottom_street('2024-04-01 00:00:00', '2024-04-02 00:00:00', 10)

    speed_distribution('2024-04-01 00:00:00', '2024-04-02 00:00:00')

    # plot_sensor_speed('400236', '2024-05-01 00:00:00', '2024-05-02 00:00:00')
    # plot_street_speed('Bayshore Freeway', '2024-06-29 00:00:00', '2024-06-30 00:00:00')
