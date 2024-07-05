import numpy as np
import os


def save_data_as_npz(filename):
    data = np.load('PEMSBAY_2024.npy')
    x_offsets = np.arange(-11, 1, 1).reshape(-1, 1)
    y_offsets = np.arange(1, 13, 1).reshape(-1, 1)

    history_length = 12
    forecast_length = 12

    num_samples = data.shape[0] - (history_length + forecast_length - 1)
    x = np.zeros((num_samples, history_length, data.shape[1], data.shape[2] - 1))
    y = np.zeros((num_samples, forecast_length, data.shape[1], data.shape[2] - 1))

    for i in range(num_samples):
        x[i] = data[i:i + history_length, :, -2:]
        y[i] = data[i + history_length:i + history_length + forecast_length, :, -2:]

    print(x.shape)
    print(y.shape)
    print(x_offsets.shape)
    print(y_offsets.shape)

    np.savez(filename, x=x, y=y, x_offsets=x_offsets, y_offsets=y_offsets)


def split_data(npz_file, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    data = np.load(npz_file)
    x = data['x']
    y = data['y']

    num_samples = x.shape[0]
    num_train = int(num_samples * train_ratio)
    num_val = int(num_samples * val_ratio)
    num_test = num_samples - num_train - num_val

    x_train, y_train = x[:num_train], y[:num_train]
    x_val, y_val = x[num_train:num_train + num_val], y[num_train:num_train + num_val]
    x_test, y_test = x[-num_test:], y[-num_test:]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for cat in ["train", "val", "test"]:
        _x, _y = locals()["x_" + cat], locals()["y_" + cat]
        print(f"{cat} x: {_x.shape}, y: {_y.shape}")
        np.savez_compressed(
            os.path.join(output_dir, f"{cat}.npz"),
            x=_x,
            y=_y
        )


if __name__ == '__main__':
    npz_file = 'PEMS-BAY-2024.npz'
    save_data_as_npz(npz_file)

    output_dir = 'pems' # 数据集划分输出到此目录下
    split_data(npz_file, output_dir, 0.7, 0.2, 0.1)
