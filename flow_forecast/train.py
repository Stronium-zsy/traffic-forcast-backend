import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from data_processing import load_and_process_data
from flow_forecast.model import SimpleNN


def train(data_path, num_epochs=20, learning_rate=0.001, batch_size=52416):
    flow_clean, speed_clean = load_and_process_data(data_path)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    speed_tensor = torch.tensor(speed_clean, dtype=torch.float32).view(-1, 1)
    flow_tensor = torch.tensor(flow_clean, dtype=torch.float32).view(-1, 1)

    dataset = TensorDataset(speed_tensor, flow_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=8)

    model = SimpleNN().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.9)

    scaler = torch.cuda.amp.GradScaler()

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for i, (speed_batch, flow_batch) in enumerate(dataloader):
            speed_batch, flow_batch = speed_batch.to(device), flow_batch.to(device)

            optimizer.zero_grad()

            with torch.cuda.amp.autocast():
                outputs = model(speed_batch)
                loss = criterion(outputs, flow_batch)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()

        scheduler.step()

        avg_loss = running_loss / len(dataloader)
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {avg_loss:.4f}')

    torch.save(model.state_dict(), 'model_para.pth')
    print('Model parameters saved to model_para.pth')


if __name__ == '__main__':
    data_path = 'PEMSBAY_2024.npy'
    train(data_path)
