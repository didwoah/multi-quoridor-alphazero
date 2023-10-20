import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pickle
from pathlib import Path
from model import resnet
from tqdm import tqdm
import os

RN_EPOCHS = 100
LEARNING_RATE = 1e-4

def load_data():
    history_path = sorted(Path('./data').glob('*.history'))[-1]
    print(history_path)
    with history_path.open(mode='rb') as f:
        return pickle.load(f)

def train_network():
    history = load_data()
    xs, y_polices, y_values = zip(*history)

    xs = np.array(xs)
    y_polices = np.array(y_polices)
    y_values = np.array(y_values)

    # Create an instance of your PyTorch model and load the model checkpoint
    model = resnet()
    # torch.save(model.state_dict(), './model/chekpoint0.pth')
    model.load_state_dict(torch.load('./model/chekpoint1.pth'))
    model.train()  # Set the model to evaluation mode
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)
    model.to(device)
    
    # Define the loss functions and optimizer
    criterion_policy = nn.CrossEntropyLoss()
    criterion_value = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    losses = []

    for epoch in range(RN_EPOCHS):
        total_loss = 0

        for x, p, v in tqdm(zip(xs, y_polices, y_values), total=len(xs), desc=f"Train {epoch + 1}/{RN_EPOCHS}"):
            # Convert data to PyTorch tensors
            x_tensor = torch.tensor(x, dtype=torch.float32)
            x_tensor = x_tensor.unsqueeze(0)
            y_polices_tensor = torch.tensor(p, dtype=torch.float32)
            y_polices_tensor = y_polices_tensor.unsqueeze(0)
            y_values_tensor = torch.tensor(v, dtype=torch.float32)
            y_values_tensor = y_values_tensor.unsqueeze(0)
            x_tensor = x_tensor.to(device)
            y_polices_tensor = y_polices_tensor.to(device)
            y_values_tensor = y_values_tensor.to(device)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            value_output, policy_output = model(x_tensor)

            # Calculate losses
            loss_policy = criterion_policy(policy_output, y_polices_tensor)
            loss_value = criterion_value(value_output, y_values_tensor)

            # Total loss
            loss = loss_policy + loss_value

            total_loss += loss.item()

            # Backpropagation
            loss.backward()
            optimizer.step()

        total_loss /= len(xs)

        losses.append(total_loss)

        print('')
        print('Train {}/{} - Loss: {:.4f}'.format(epoch + 1, RN_EPOCHS, total_loss))

    # Save the trained model
    torch.save(model.state_dict(), './model/chekpoint2.pth')
    write_data(losses)


def write_data(losses):
    os.makedirs('./data/', exist_ok=True)
    path = './data/chekpoint2.loss'
    with open(path, mode='wb') as f:
        pickle.dump(losses, f)

if __name__ == '__main__':
    train_network()