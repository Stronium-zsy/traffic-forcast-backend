import torch
from flow_pre.model import SimpleNN
from flow_pre.data_processing import adjust_flow


def load_model(model_path, device):
    model = SimpleNN().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


def infer(model, speed, device):
    with torch.no_grad():
        speed_tensor = torch.tensor([speed], dtype=torch.float32).view(-1, 1).to(device)
        flow = model(speed_tensor)
        return flow.item()


def forecast_flow(speeds):
    model_path = 'flow_pre/model_para.pth'
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = load_model(model_path, device)

    s_mean = 61.67313578355407
    s_std = 11.980457182357718
    f_mean = 215.09537798206068
    f_std = 145.6325438288676

    flows = []
    for speed in speeds:
        speed_norm = (speed - s_mean) / s_std
        flow = infer(model, speed_norm, device)
        flow = flow * f_std + f_mean
        nflow = adjust_flow(speed, flow)
        flows.append(round(nflow, 2))
    return flows
