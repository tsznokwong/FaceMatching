from tkinter import *
import cv2
from PIL import Image, ImageTk
from authentication import *

def on_click_login():
  if isLoggedIn():
    logout()
  else:
    login("abc")
  text = "Logout" if isLoggedIn() else "Login"
  button.text = text
  button.configure(text=text)

def setup_ui():
  window = Tk()

  window.title("Face ID Application")
  window.geometry("1920x1080")
  window.configure(background="white", cursor="arrow")

  panel = Label(window)
  panel.pack(padx=8, pady=8)

  text = "Logout" if isLoggedIn() else "Login"
  button = Button(window, text=text, command=on_click_login)
  button.pack(fill="both", expand=True, padx=8, pady=8)

  camera = cv2.VideoCapture(0)
  return window, camera, panel, button

window, camera, panel, button = setup_ui()