from model import *
from checkpoint_manager import *
from view_controller import *
from PIL import Image, ImageTk

device = "cpu"
threshold = 0.399934

save_path = f"./contrastive-loss-0.50-2021-03-23-13_17_20.pt"
load_model = SiameseNet().to(device)
load_checkpoint(save_path, load_model)

view_controller = ViewController()
view_controller.start()



