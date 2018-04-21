#!/usr/bin/env python3

import math
import serial
import tkinter as tk
from tkinter import filedialog
from random import randint

MAX_NODES = 7
NODE_RADIUS = 50
NODE_UNACTIVATED = 'blue'
NODE_ACTIVATED = 'green'
PIXEL_SCALE = 4.07 # meter

class Application(tk.Frame):
    def __init__(self, master=None):
        self.c_width = 1500
        self.c_height = 900

        self.prev = None

        self.node_pos = []
        self.nodes = []
        
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.draw_map()

    def create_widgets(self):
        self.map_area = tk.Canvas(self, width=self.c_width, height=self.c_height)
        self.map_area.pack(expand=tk.YES, fill=tk.BOTH)

        self.new_nodes = tk.Button(self, text='New Nodes', command=self.define_nodes)
        self.new_nodes.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.new_nodes = tk.Button(self, text='Save Nodes', command=self.save_nodes)
        self.new_nodes.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.new_nodes = tk.Button(self, text='Load Nodes', command=self.load_nodes)
        self.new_nodes.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.new_nodes = tk.Button(self, text='Shortest Path', command=self.show_shortest_path)
        self.new_nodes.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def draw_map(self):
        self.bg_img = tk.PhotoImage(file='gbg_map.gif')
        self.map_area.create_image(0, 0, image=self.bg_img, anchor=tk.NW)
        
    def draw_nodes(self):
        self.nodes = []
        n = 0
        for pos in self.node_pos:
            x, y = pos[0], pos[1]
            node = self.map_area.create_oval(x-25, y-25, x+25, y+25,  fill=NODE_UNACTIVATED)
            self.map_area.create_text(x, y, text=str(n), fill='white', font='20')
            self.nodes.append(node)
            n += 1

    # Run this when one node has been activated
    def touched(self, cid):
        self.map_area.itemconfig(cid, fill=NODE_ACTIVATED)
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

    def define_nodes(self):
        self.node_pos = []
        self.draw_map()
        self.map_area.bind('<Button 1>', self.place_node)

    def stop_define_nodes(self):
        self.map_area.unbind('<Button 1>')

    def place_node(self, event):
        x, y = event.x, event.y
        self.node_pos.append([x,y])
        print('node at: {},{}'.format(x, y))
        if len(self.node_pos) >= MAX_NODES:
            self.stop_define_nodes()
            print('All nodes placed!')
        self.draw_nodes()

    def save_nodes(self):
        try:
            with filedialog.asksaveasfile(defaultextension='.csv') as savefile:
                for pos in self.node_pos:
                    x, y = pos[0], pos[1]
                    savefile.write('{},{}\n'.format(x, y))
            print('Nodes saved!')
        except:
            print('Nodes not saved!')

    def load_nodes(self):
        try:
            with filedialog.askopenfile() as savefile:
                self.node_pos = []
                for line in savefile:
                    pos = line.strip().split(',')
                    x, y = int(pos[0]), int(pos[1])
                    self.node_pos.append([x, y])
                self.draw_map()
                self.draw_nodes()
            print('Nodes loaded!')
        except:
            print('No nodes loaded!')
            pass

    def show_shortest_path(self):
        length, path = self.shortest_path()
        self.map_area.create_text(10,30, text='Shortest path: {}, length: {:.2f} m'.format(path, length*PIXEL_SCALE), font=('Courier', 30), anchor=tk.NW)


    def shortest_path(self, path_str=None, nbrs_left=None):
        # Start off really big
        shortest = 1e16

        if (not path_str) and (not nbrs_left):
            path_str = '0'
            nbrs_left = ''
            for n in range(1,len(self.nodes)):
                nbrs_left += str(n)
            print(len(self.nodes))

        if (not nbrs_left) and (len(path_str) > 1):
            shortest = self.get_path_length(path_str)
            shortest_str = path_str
        elif nbrs_left:
            for n in nbrs_left:
                new_str = path_str + n
                new_left = nbrs_left.replace(n,'')
                path_len, short_str = self.shortest_path(new_str, new_left)
                if path_len < shortest:
                    shortest = path_len
                    shortest_str = short_str

        return shortest, shortest_str


    def get_path_length(self, path_str):
        dist = 0
        for i in range(len(path_str)):
            n1 = path_str[i]
            n2 = path_str[(i+1)%len(path_str)]
            dist += self.get_distance(self.node_pos[int(n1)], self.node_pos[int(n2)])
        return dist
            
    def get_distance(self, a, b):
        x1, y1 = a[0], a[1]
        x2, y2 = b[0], b[1]
        return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

try:        
    ser = serial.Serial('/dev/ttyACM0')
except:
    pass
            
root = tk.Tk()
app = Application(master=root)
app.draw_map()
if len(app.node_pos) > 0:
    app.draw_nodes()



while True:
    app.update_idletasks()
    app.update()
    try:
        data = ser.readline()
        print(data.decode().strip())
        id_nbr = int(data.decode().strip())
        
        if id_nbr:
            app.touched(int(data.decode().strip()) % 10)
    except:
        id_nbr = None
        pass
