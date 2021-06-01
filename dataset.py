import pandas as pd
from PIL import Image
import numpy as np
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import os

class FaceDataset(Dataset):

  def __init__(self, csv_file, index_file = INDEX_FILE_PATH):
    # import csv
    self.df = pd.read_csv(csv_file)  

    # import index file           
    index_df = pd.read_csv(index_file, header=None).set_index([0]);   
    index_df.columns = ["path"] 
    self.path_dict = index_df.to_dict("index")

  def __getimage__(self, id):
    image_path = os.path.join(PATH, self.path_dict[id]["path"])
    image = Image.open(image_path) \
      .resize((32, 32)) \
      .convert("L")

    transform = transforms.Compose([ transforms.ToTensor() ])
    image = transform(image)
    
    return image

  def __getitem__(self, idx):
    entry = self.df.iloc[idx]
    return self.__getimage__(entry[0]), self.__getimage__(entry[1]), np.float32(entry[2])

  def __len__(self):
    return len(self.df)
