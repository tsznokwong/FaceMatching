from model import *
from dataset import *
from torch.utils.data import DataLoader

class Authenticator():

  def __init__(self, batch_size):
    self.matching = False
    self.batch_size = batch_size
    self.user_id = ""
    self.user_dict = {}
    self.device = "cpu"
    # self.threshold = 0.399934
    self.threshold = 0.8

    self.save_path = f"./contrastive-loss-0.50-2021-03-23-13_17_20.pt"
    self.model = SiameseNet().to(self.device)
    load_checkpoint(self.save_path, self.model)

  def isLoggedIn(self):
    return self.user_id != ""

  def login(self, user_id):
    self.user_id = user_id
    print(f"{self.user_id} Login")

  def logout(self):
    print(f"{self.user_id} Logout")
    self.user_id = ""

  def get_user_id(self):
    return self.user_id

  def register(self, user_id, frames):
    self.user_dict[user_id] = frames

  def can_match(self):
    return not self.isLoggedIn() and not self.matching

  def match(self, frame):
    if not self.can_match():
      return
    self.matching = True
    for (key, frames) in self.user_dict.items():
      dataset = FaceDataset(frames, frame)
      loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
      count = self.__pred__(loader)
      if count > self.batch_size * 0.8:
        self.login(key)
        break
    self.matching = False
    return self.isLoggedIn()

  def __pred__(self, loader):
    self.model.eval()
    all_outputs = torch.empty(0)
    for images1, images2, _ in loader:
      images1, images2 = images1.to(self.device), images2.to(self.device)
      outputs = self.model((images1, images2)) 
      all_outputs = torch.cat((all_outputs, outputs.cpu().detach()))
    casted_outputs = torch.where(all_outputs > self.threshold, 1, 0)
    return torch.sum(casted_outputs)
