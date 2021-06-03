from tkinter import *
import tkinter.ttk as ttk
import cv2
from PIL import Image, ImageTk
from authentication import *
from threading import Timer, Thread

class ViewController():

  def __init__(self):
    self.batch_size = 128
    self.auth = Authenticator(self.batch_size)
    self.window = Tk()

    self.window.title("Face ID Application")
    self.window.geometry("600x800")
    self.window.configure(background="white", cursor="arrow")

    self.panel = Label(self.window)
    self.panel.pack(padx=8, pady=8)
    self.panel_counter = 0

    self.register_button = Button(self.window, text="Register", command=self.on_click_register)
    self.register_button.pack(padx=8, pady=8)

    self.counter = None
    self.count_down_label = Label(self.window, text="0")
    self.count_down_label.pack(padx=8, pady=8)

    self.recording = False
    self.recording_progress = ttk.Progressbar(self.window, maximum=self.batch_size)
    self.recording_progress.pack(padx=8, pady=8)
    self.recording_frames = []

    self.user_id_field = Text(self.window, height=1)
    self.user_id_field.configure(background="grey")
    self.user_id_field.pack(padx=8, pady=8)
    self.confirm_button = Button(self.window, text="Confirm Register", command=self.on_click_confirm)
    self.confirm_button.pack(padx=8, pady=8)

    self.camera = cv2.VideoCapture(0)
    self.update_ui()

  def update_ui(self):
    self.update_register_button()
    self.update_counter()
    self.update_progress()
    self.update_user_id_field()
    
  def update_register_button(self):
    text = f"Logout {self.auth.get_user_id()}" if self.auth.isLoggedIn() else "Register"
    self.register_button.text = text
    self.register_button.configure(text=text)

  def update_counter(self):
    if self.counter == None:
      self.count_down_label.pack_forget()
    else:
      text = str(self.counter)
      self.count_down_label.text = text
      self.count_down_label.configure(text=text)
      self.count_down_label.pack()

  def update_progress(self):
    if self.recording:
      self.recording_progress.pack()
    else:
      self.recording_progress.pack_forget()
  
  def update_user_id_field(self):
    if len(self.recording_frames) == self.batch_size:
      self.user_id_field.pack()
      self.confirm_button.pack()
    else:
      self.user_id_field.pack_forget()
      self.confirm_button.pack_forget()
    
  def count_down(self):
    self.counter -= 1
    if self.counter == 0:
      self.counter = None
      self.update_counter()
      self.recording = True
      self.recording_progress.value = 0
      self.recording_progress.configure(value=0)
      self.update_progress()
      return
    self.update_counter()
    t = Timer(1, self.count_down)
    t.start()
   
  def on_click_register(self):
    if self.auth.isLoggedIn():
      self.auth.logout()
      self.update_register_button()
    else:
      self.register_button.pack_forget()
      self.counter = 4
      self.count_down()
      self.update_counter()

  def on_click_confirm(self):
    user_id = self.user_id_field.get("1.0", "end-1c")
    self.auth.register(user_id, self.recording_frames)
    self.recording_frames = []
    self.register_button.pack()
    self.update_ui()

  def video_loop(self):
    success, frame = self.camera.read()
    if success:
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      image = Image.fromarray(image)
      image = crop_square(image)
      image = image.transpose(Image.FLIP_LEFT_RIGHT)
      self.panel_counter = (self.panel_counter + 1) % 20

      imgtk = ImageTk.PhotoImage(image=image)
      self.panel.imgtk = imgtk
      self.panel.configure(image=imgtk)
      self.window.after(50, self.video_loop)
      if self.recording:
        self.recording_frames.append(image)
        self.recording_progress.step()
        if (self.batch_size == len(self.recording_frames)):
          self.recording = False
          self.update_progress()
          self.update_user_id_field()
      elif self.counter == None and len(self.recording_frames) == 0 and self.panel_counter == 0 and not self.auth.isLoggedIn():
        t = Thread(target=self.match, args=(image,))
        t.start()

  def match(self, image):
    if self.auth.can_match():
      success = self.auth.match(image)
      if success:
        self.update_ui()

  def start(self):
    self.video_loop()
    self.window.mainloop()
    self.camera.release()
    cv2.destroyAllWindows()


def crop_square(image):
  width, height = image.size
  square_length = min(width, height) * 0.75
  left = (width - square_length) / 2
  top = (height - square_length) / 2
  right = (width + square_length) / 2
  bottom = (height + square_length) / 2
  return image.crop((left, top, right, bottom))
