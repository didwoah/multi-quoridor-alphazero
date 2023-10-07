import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import LambdaLR
import numpy as np
import pickle
from pathlib import Path
from quoridor.model import DN_INPUT_SHAPE
from quoridor.model import resnet

RN_EPOCHS = 100
a, b, c = DN_INPUT_SHAPE

def load_data():
    history_path = sorted(Path('./data').glob('*.history'))[-1]
    with history_path.open(mode='rb') as f:
        return pickle.load(f)

def step_decay(epoch):
    x = 0.001
    if epoch >= 50:
        x = 0.0005
    if epoch >= 80:
        x = 0.00025
    return x

def train_network():
    history = load_data()
    xs, y_polices, y_values = zip(*history)

    xs = np.array(xs)
    xs = xs.reshape(len(xs), c, a, b).transpose(0, 2, 3, 1)
    y_polices = np.array(y_polices)
    y_values = np.array(y_values)

    # Create an instance of your PyTorch model and load the model checkpoint
    model = resnet()
    model.load_state_dict(torch.load('your_model_checkpoint.pth'))
    model.train()  # Set the model to evaluation mode
    
    # Define the loss functions and optimizer
    criterion_policy = nn.CrossEntropyLoss()
    criterion_value = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    # Create a learning rate scheduler
    lr_scheduler = LambdaLR(optimizer, lr_lambda=step_decay)

    num_epochs = RN_EPOCHS

    for epoch in range(num_epochs):
        print(f"Train {epoch + 1}/{num_epochs}", end='')
        
        # Convert data to PyTorch tensors
        xs_tensor = torch.tensor(xs, dtype=torch.float32)
        y_polices_tensor = torch.tensor(y_polices, dtype=torch.long)
        y_values_tensor = torch.tensor(y_values, dtype=torch.float32)

        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        policy_output, value_output = model(xs_tensor)

        # Calculate losses
        loss_policy = criterion_policy(policy_output, y_polices_tensor)
        loss_value = criterion_value(value_output, y_values_tensor)

        # Total loss
        loss = loss_policy + loss_value

        # Backpropagation
        loss.backward()
        optimizer.step()

        print('\rTrain {}/{} - Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()), end='')

    # Save the trained model
    torch.save(model.state_dict(), './model/latest.pth')

if __name__ == '__main__':
    train_network()
