import argparse
import torch
import numpy as np
import util
from engine import trainer


def get_time_step(predict_time):
    time_steps = {'15min': 3, '30min': 6, '1h': 12}
    if predict_time in time_steps:
        return time_steps[predict_time]
    else:
        raise ValueError("Invalid predict time. Choose from '15min', '30min', '1h'.")


def set_random_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)


def load_data_and_supports(data_path, adjdata, adjtype, device, batch_size):
    if adjdata:
        sensor_ids, sensor_id_to_ind, adj_mx = util.load_adj(adjdata, adjtype)
        supports = [torch.tensor(i).to(device) for i in adj_mx]
    else:
        supports = None

    dataloader = util.load_dataset(data_path, batch_size, batch_size, batch_size)
    scaler = dataloader['scaler']

    return dataloader, scaler, supports


def load_model(args, device, scaler):
    model = trainer(scaler,
                    in_dim=args.in_dim,
                    seq_length=args.seq_length,
                    num_nodes=args.num_nodes,
                    nhid=args.nhid,
                    dropout=args.dropout,
                    device=device,
                    lr_mul=args.lr_mul,
                    n_warmup_steps=args.n_warmup_steps,
                    quantile=args.quantile,
                    is_quantile=args.is_quantile,
                    warmup_epoch=args.warmup_epoch).model

    model.load_state_dict(torch.load(args.load_path, map_location=device))
    model.to(device)
    model.eval()

    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda:0', help='Device to use for computation')
    parser.add_argument('--data', type=str, default='data/PEMS-BAY', help='Data path')
    parser.add_argument('--adjdata', type=str, default='data/PEMS-BAY/adj_mx.pkl', help='Adjacency data path')
    parser.add_argument('--adjtype', type=str, default='doubletransition', help='Adjacency type')
    parser.add_argument('--seq_length', type=int, default=12, help='Sequence length')
    parser.add_argument('--nhid', type=int, default=32, help='Number of hidden units')
    parser.add_argument('--in_dim', type=int, default=2, help='Input dimension')
    parser.add_argument('--num_nodes', type=int, default=325, help='Number of nodes')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--dropout', type=float, default=0.3, help='Dropout rate')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--seed', type=int, default=99, help='Random seed')
    parser.add_argument('--save', type=str, default='./experiment/METR-LA_TESTAM', help='Save path')
    parser.add_argument('--load_path', type=str,
                        default='C:/Users/27135/Desktop/实训/PEMS-BAY_result/BEST_PEMS-BAY_1.55.pth')
    parser.add_argument('--lr_mul', type=float, default=1, help='Learning rate multiplier')
    parser.add_argument('--n_warmup_steps', type=int, default=4000, help='Number of warm-up steps')
    parser.add_argument('--quantile', type=float, default=0.7, help='Quantile value')
    parser.add_argument('--is_quantile', action='store_true', help='Use quantile regression')
    parser.add_argument('--warmup_epoch', type=int, default=0, help='Number of warm-up epochs')
    parser.add_argument('--predict_time', type=str, default='15min', choices=['15min', '30min', '1h'],
                        help='Predict time')
    args = parser.parse_args()

    set_random_seed(args.seed)

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')

    dataloader, scaler, supports = load_data_and_supports(args.data, args.adjdata, args.adjtype, device,
                                                          args.batch_size)

    model = load_model(args, device, scaler)

    time_step = get_time_step(args.predict_time)

    results = []
    with torch.no_grad():
        for iter, (x, y) in enumerate(dataloader['val_loader'].get_iterator()):
            testx = torch.Tensor(x).to(device).transpose(1, 3)[:, :, :, -12:]
            preds = model(testx)[:, :, :, time_step - 1]
            results.append(preds.cpu().numpy())

    results = scaler.inverse_transform(np.concatenate(results, axis=0))

    print(f"Inference results for {args.predict_time}:")
    print(results)


if __name__ == "__main__":
    main()
