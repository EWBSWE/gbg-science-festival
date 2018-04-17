#!/usr/bin/env python3

import serial
import tkinter as tk
from random import randint

class Application(tk.Frame):
    def __init__(self, master=None):
        self.c_width = 500
        self.c_height = 500

        self.circles = []
        
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.map_area = tk.Canvas(self, bg='white', height='500', width='500')
        self.map_area.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def draw_circles(self):
        nbr_circles = 8
        for i in range(nbr_circles):
            x = randint(0, self.c_width - 50) + 25
            y = randint(0, self.c_height - 50) + 25
            circ = self.map_area.create_oval(x-25, y-25, x+25,
                                                     y+25,  fill='blue')
            self.circles.append(circ)

    def touched(self, cid):
        self.map_area.itemconfig(cid, fill='red')

    def reset(self):
        pass
        
ser = serial.Serial('/dev/ttyACM0')

            
root = tk.Tk()
app = Application(master=root)
app.draw_circles()
while True:

    app.update_idletasks()
    app.update()
    data = ser.readline()
    print(data.decode().strip())
    try:
        id_nbr = int(data.decode().strip())
        if isinstance(int(data.decode().strip()), int):
            app.touched(int(data.decode().strip()) % 10)
    except:
        pass
        
