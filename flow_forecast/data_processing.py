import numpy as np


def zscore(flow, speed):
    nor_flow = (flow - np.mean(flow)) / np.std(flow)
    nor_speed = (speed - np.mean(speed)) / np.std(speed)
    return nor_flow, nor_speed


def load_and_process_data(filepath):
    data = np.load(filepath)
    flow = data[:, :, 0]
    speed = data[:, :, 1]

    flow, speed = zscore(flow, speed)

    flow_flat = flow.flatten().astype(np.float32)
    speed_flat = speed.flatten().astype(np.float32)

    return flow_flat, speed_flat


def adjust_flow(speed, flow):
    if speed <= 30:
        coefficient = 0.75 + 0.25 * (speed / 30)
    elif 30 < speed <= 40:
        coefficient = 1.0 + 0.1 * (speed - 30) / 10
    elif 40 < speed <= 50:
        coefficient = 1.1 + 0.15 * (speed - 40) / 10
    elif 50 < speed <= 60:
        coefficient = 1.2 + 0.4 * (speed - 50) / 10
    elif 60 < speed <= 66:
        coefficient = 1.5 + 1.5 * (speed - 60) / 10
    elif 66 < speed <= 67:
        coefficient = 3.5 + 0.5 * (speed - 66)
    elif 67 < speed <= 68:
        coefficient = 4.0 + 0.5 * (speed - 67)
    elif 68 < speed <= 69:
        coefficient = 4.5 + 0.5 * (speed - 68)
    else:
        coefficient = 4.0 + 0.05 * (speed - 70) / 10

    adjusted_flow = flow * coefficient
    return adjusted_flow
