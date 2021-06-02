import torch
import torch.nn as nn
import torch.nn.functional as F

def aggregate(h1, h2):
  return torch.abs(torch.sub(h1, h2))


class ConvNet(nn.Module):
  def __init__(self):
    super(ConvNet, self).__init__()
    
    # Input 1 x 32 x 32 image
    # Conv 3 x 3 kernel size, 32 kernels, stride 1, padding 1
    self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
    # Batch Norm
    self.norm1 = nn.BatchNorm2d(32)

    # Conv 3 x 3 kernel size, 32 kernels, stride 1, padding 1
    self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1)
    # Batch Norm
    self.norm2 = nn.BatchNorm2d(32)

    # Max pooling, 2 x 2 kernel size, stride 2, padding 0
    self.maxPool = nn.MaxPool2d(kernel_size=2, stride=2)

    # Conv 3 x 3 kernel size, 64 kernels, stride 1, padding 1
    self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
    # Batch Norm
    self.norm3 = nn.BatchNorm2d(64)

    # Conv 3 x 3 kernel size, 128 kernels, stride 1, padding 1
    self.conv4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
    # Batch Norm
    self.norm4 = nn.BatchNorm2d(128)

    # Conv 3 x 3 kernel size, 256 kernels, stride 1, padding 1
    self.conv5 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
    # Batch Norm
    self.norm5 = nn.BatchNorm2d(256)

    # Conv 3 x 3 kernel size, 512 kernels, stride 1, padding 1
    self.conv6 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1)
    # Batch Norm
    self.norm6 = nn.BatchNorm2d(512)

    # Average pooling, 16 x 16 kernel size, stride /, padding 0
    self.avgPool = nn.AvgPool2d(kernel_size=16)

  def forward(self, x):
    x = F.relu(self.norm1(self.conv1(x)))
    x = F.relu(self.norm2(self.conv2(x)))
    x = self.maxPool(x)
    x = F.relu(self.norm3(self.conv3(x)))
    x = F.relu(self.norm4(self.conv4(x)))
    x = F.relu(self.norm5(self.conv5(x)))
    x = F.relu(self.norm6(self.conv6(x)))
    x = self.avgPool(x)
    x = x.view(-1, 512)
    return x


class FCNet(nn.Module):
  def __init__(self):
    super(FCNet, self).__init__()
    
    # Input 512
    # FC 512 hidden units, dropout 0.5
    self.fc1 = nn.Linear(512, 512)
    self.drop = nn.Dropout(0.5)

    # output 1
    self.fc2 = nn.Linear(512, 1)

  def forward(self, x):
    x = self.drop(F.relu(self.fc1(x)))
    x = torch.sigmoid(self.fc2(x))
    x = torch.flatten(x)
    return x
    

class SiameseNet(nn.Module):
  def __init__(self):
    super(SiameseNet, self).__init__()
    
    self.conv = ConvNet()
    self.fc = FCNet()

  def forward(self, x):
    self.h1 = self.conv(x[0])
    self.h2 = self.conv(x[1])
    x = aggregate(self.h1, self.h2)
    x = self.fc(x)
    return x

def save_checkpoint(path, model, optimizer, train_loss_history, valid_loss_history, valid_loss, verbose = 1):
    if path == None:
      return
    state_dict = { \
      "model_state": model.state_dict(), \
      "optimizer_state": optimizer.state_dict(), \
      "valid_loss": valid_loss, \
      "train_loss_history": train_loss_history, \
      "valid_loss_history": valid_loss_history \
    }
    torch.save(state_dict, path)
    if verbose > 0:
      print(f"Model saved to {path}")

def load_checkpoint(path, model, optimizer = None, device = "cpu", verbose = 1):
    state_dict = torch.load(path, map_location=device)
    model.load_state_dict(state_dict["model_state"])
    if optimizer != None:
      optimizer.load_state_dict(state_dict["optimizer_state"])
    valid_loss = state_dict["valid_loss"]
    valid_loss_history = state_dict["valid_loss_history"]
    train_loss_history = state_dict["train_loss_history"]
    if verbose > 0:
      print(f"Model loaded from {path}, with Validation Loss: {valid_loss}")
    return train_loss_history, valid_loss_history, valid_loss
