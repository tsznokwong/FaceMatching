from PIL import Image
import numpy as np
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class FaceDataset(Dataset):

  def __init__(self, reference_frames, frame):
    self.reference_frames = reference_frames
    self.image = frame \
      .resize((32, 32)) \
      .convert("L")

    transform = transforms.Compose([ transforms.ToTensor() ])
    self.image = transform(self.image)

  def __getimage__(self, id):
    image = self.reference_frames[id] \
      .resize((32, 32)) \
      .convert("L")

    transform = transforms.Compose([ transforms.ToTensor() ])
    image = transform(image)
    return image

  def __getitem__(self, idx):
    return self.__getimage__(idx), self.image, -1

  def __len__(self):
    return len(self.reference_frames)
