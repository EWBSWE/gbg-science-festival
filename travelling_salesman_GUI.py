#!/usr/bin/env python3

import serial
import tkinter as tk
from random import randint

class Application(tk.Frame):
    def __init__(self, master=None):
        self.c_width = 500
        self.c_height = 500

        self.prev = None

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
        print(self.prev, cid)
        if self.prev and (cid != self.prev):

            prev_coords = self.map_area.coords(self.prev)
            curr_coords = self.map_area.coords(cid)
            x1 = prev_coords[0] + 25
            y1 = prev_coords[1] + 25
            x2 = curr_coords[0] + 25
            y2 = curr_coords[1] + 25
            self.map_area.create_line(x1, y1, x2, y2, fill='black')
            self.prev = cid
            print(x1, y1, x2, y2)            
        else:
            self.prev = cid

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
        
    except:
        id_nbr = None
        pass
    if id_nbr:
        app.touched(int(data.decode().strip()) % 10)
        
