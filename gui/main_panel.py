from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import pandas as pd
import cv2
import sys
import glob
import time



# get pi list
pi_list = pd.read_csv("pi_list.conf")


main_window = tk.Tk()
main_window.config(width = 320, height =240)
main_window.title("NBO camera GUI")
combo = ttk.Combobox(
        state = "readonly",
        width = 50,
        font = "Verdana 24 bold",
        values = pi_list["pi_name"].values.tolist()
        )
combo.place(x=0,y=0)

# button

# button fun
def get_pi():
    pi_name = combo.get()
    pi_ip = pi_list.loc[pi_list['pi_name'] == pi_name, 'ip'].iloc[0]
    pi_label.config(text = pi_ip)
    for img in glob.glob('/home/nicoluarte/raspberry_images/*.jpg'):
        print(img)
        imm = cv2.imread(img)
        cv2.imshow('image', imm)
        cv2.waitKey(0)
        time.sleep(1)
        cv2.destroyAllWindows()


button_select_pi = tk.Button(
        main_window,
        text = "Select pi",
        width = 10,
        height = 1,
        font = "Verdana 24 bold",
        command = get_pi
        )
button_select_pi.place(x=0,y=100)

# label
pi_label = tk.Label(
        main_window,
        text = ". . .",
        font = "Verdana 24 bold"
        )
pi_label.place(x=0,y=300)

main_window.mainloop()

