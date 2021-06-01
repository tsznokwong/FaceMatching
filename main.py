from model import *
from checkpoint_manager import *
from ui_manager import *
from PIL import Image, ImageTk

device = "cpu"
threshold = 0.399934

save_path = f"./contrastive-loss-0.50-2021-03-23-13_17_20.pt"
load_model = SiameseNet().to(device)
load_checkpoint(save_path, load_model)

def video_loop():
  success, frame = camera.read()
  if success:
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=image)
    panel.imgtk = imgtk
    panel.configure(image=imgtk)
    cv2.waitKey(100)
    window.after(100, video_loop)

video_loop()
window.mainloop()
camera.release()
cv2.destroyAllWindows()



