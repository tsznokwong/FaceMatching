from tkinter import *
import cv2
from PIL import Image, ImageTk
from authentication import *

class ViewController():

  def __init__(self):
    self.auth = Authenticator()
    self.window = Tk()

    self.window.title("Face ID Application")
    self.window.geometry("600x800")
    self.window.configure(background="white", cursor="arrow")

    self.panel = Label(self.window)
    self.panel.pack(padx=8, pady=8)

    self.register_button = Button(self.window, text="Login", command=self.on_click_register)
    self.register_button.pack(padx=8, pady=8)

    self.camera = cv2.VideoCapture(0)
    self.update_ui()

  def update_ui(self):
    text = "Logout" if self.auth.isLoggedIn() else "Register"
    self.register_button.text = text
    self.register_button.configure(text=text)

   
  def on_click_register(self):
    if self.auth.isLoggedIn():
      self.auth.logout()
    else:
      self.auth.login("abc")
    self.update_ui()

  def video_loop(self):
    success, frame = self.camera.read()
    if success:
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
      image = Image.fromarray(image)
      image = crop_square(image)
      image = image.transpose(Image.FLIP_LEFT_RIGHT)
      imgtk = ImageTk.PhotoImage(image=image)
      self.panel.imgtk = imgtk
      self.panel.configure(image=imgtk)
      cv2.waitKey(100)
      self.window.after(100, self.video_loop)

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
