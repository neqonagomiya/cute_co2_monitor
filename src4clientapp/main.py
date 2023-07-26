import tomli
from client import Client
import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
import io
import time
import sys
import threading
import winsound
# setting Config =====================================================
#os.path.join(os.path.dirname(os.path.realpath("__file__")), "img") 
with open("./setting/setting.toml","rb") as f:
    tomlist = tomli.load(f)

"""
winsound.PlaySound(wav_dir+wav_level3, winsound.SND_FILENAME)
"""
# wav path
wav_dir = tomlist["wav"]["wav_dir"]
wav_level1 = tomlist["wav"]["wav_level1"] 
wav_level2 = tomlist["wav"]["wav_level2"]
wav_level3 = tomlist["wav"]["wav_level3"]

# img path
img_dir = tomlist["img"]["img_dir"]
img_base = tomlist["img"]["img_base"]
img_level1 = tomlist["img"]["img_level1"]
img_level2 = tomlist["img"]["img_level2"]
img_level3 = tomlist["img"]["img_level3"]

# napkin client path
HTTP = "https://"
HOST = tomlist["napkin"]["HOST"]
PATH = tomlist["napkin"]["PATH"]
ways = tomlist["napkin"]["ways"]
periods = tomlist["napkin"]["periods"]
data_type = tomlist["napkin"]["data_type"] #"Humidity", "Temperature"
PORT = tomlist["napkin"]["PORT"]
API_KEY = tomlist["napkin"]["API_KEY"]
DEVICE_ID = tomlist["napkin"]["DEVICE_ID"]

napkin_client = Client(HTTP, HOST, PATH, ways, periods,
                       data_type, PORT, API_KEY, DEVICE_ID)

monitor_duration = 60 * 3
# setting GUI =========================================================

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def show_img():
    global item, canvas
    app = ctk.CTk()
    app.title("CO2 Monitor")
    app.geometry("250x250")

    img = Image.open(img_dir+img_base)
    img = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(app,width=500, height=500)
    canvas.place(x=25, y=25)
    item = canvas.create_image(0,0, image=img, anchor=tkinter.NW)
    app.mainloop()


# main ----------------------------------------------------------------

thread1 = threading.Thread(target=show_img)
thread1.start()

while True:
    try:
        mean_val = napkin_client.get_mean()

        if mean_val>=0 and mean_val<1000:
            print("level 1")
            img1 = Image.open(img_dir+img_level1)
            img1 = ImageTk.PhotoImage(img1)
            canvas.itemconfig(item, image=img1)
            winsound.PlaySound(wav_dir+wav_level1,
                               winsound.SND_FILENAME)
        elif mean_val>=1000 and mean_val<2000:
            print("level2")
            img2 = Image.open(img_dir+img_level2)
            img2 = ImageTk.PhotoImage(img2)
            canvas.itemconfig(item, image=img2)
            winsound.PlaySound(wav_dir+wav_level2,
                                winsound.SND_FILENAME)
        else:
            print("level3")
            img3 = Image.open(img_dir+img_level3)
            img3 = ImageTk.PhotoImage(img3)
            canvas.itemconfig(item, image=img3)
            winsound.PlaySound(wav_dir+wav_level3,
                               winsound.SND_FILENAME)
        time.sleep(4)
        
        img = Image.open(img_dir + img_base)
        img = ImageTk.PhotoImage(img)
        canvas.itemconfig(item,image=img)

        time.sleep(monitor_duration)

    except KeyboardInterrupt:
        print("Exit")

