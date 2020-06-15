# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 23:18:16 2020

@author: Kevin
"""

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog
class MyPage():
    
    def __init__(self):
        
        self.root = tkinter.Tk()
        self.root.filename="No file loaded yet"
       
        
        self.root.wm_title("Filter Tester")
        self.start_value = np.random.randint(0,1000,size=10000)
        self.file_loaded = False        
        
        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.ax = self.fig.add_subplot(111)
        
        self.ax.plot(self.start_value)
        self.ax.title.set_text("No filter used")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.canvas.mpl_connect("key_press_event", self.on_key_press)

        self.cnt = 1

        self.ax.grid()
    def on_key_press(self,event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)
    

    def quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    def increase(self):

        self.cnt += 1
        mask = [1]*self.cnt        
        res = np.convolve(self.start_value,mask,"valid") / self.cnt
        print(res)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(res)
        self.ax.title.set_text(str("Filter length: " + str(self.cnt)+ "\nfilename: " + self.root.filename))
        if self.file_loaded == True:
            self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
            self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.grid()
        self.canvas.draw()
 
    def decrease(self):

        if self.cnt == 1:
            return 
        self.cnt -= 1
        mask = [1]*self.cnt        
        res = np.convolve(self.start_value,mask,"valid") / self.cnt
        print(res)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(res)
        self.ax.title.set_text(str("Filter length: " + str(self.cnt)+ "\nfilename: " + self.root.filename))
        if self.file_loaded == True:
            self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
            self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.grid()
        self.canvas.draw()
       
    def gaussianFilter(self):
        
        start_mask = [1,1]
        
        res = [1,1]
        if self.cnt < 3:
            tkinter.alert("NO")
        for i in range(self.cnt-1):
            res = np.convolve(res,start_mask)
        
        print("Mask:",res)
        mask = res
        res = res / res.sum()
        res = np.convolve(self.start_value,res,"valid") / self.cnt
        
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(res)
        self.ax.title.set_text(str("Gaussian Filter: " + str(mask)+ "\nfilename: " + self.root.filename))
        if self.file_loaded == True:
            self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
            self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.grid()
        self.canvas.draw()
    
    def customSized(self,sv):
        
        try:
            val = int(sv.get())
        except Exception as e:
            print(e)
            return
        
        mask = [1]*val       
        res = np.convolve(self.start_value,mask,"valid") / val
        print(res)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(res)
        self.ax.title.set_text(str("Filter length: " + str(val)+ "\nfilename: " + self.root.filename))
        if self.file_loaded == True:
            self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
            self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.grid()
        self.canvas.draw()       
        self.cnt = val

    def customFilter(self,sv):
        
        try:
            vals = sv.get().split(",")
            mask = [float(i) for i in vals]
        except Exception as e:
            print(e)
            return
        print(mask)
        res = np.convolve(self.start_value,mask,"valid")
        print(res)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(res)
        self.ax.title.set_text(str("Filter: " + str(mask)+ "\nfilename: " + self.root.filename))
        if self.file_loaded == True:
            self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
            self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.grid()
        self.canvas.draw()   

    def LoadFile(self):
        self.root.filename = tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("CSV files","*.csv"),("all files","*.*")))
        print(self.root.filename)

        with open(start.root.filename,"r") as f:
            data = f.readlines()

        self.lines = []       
        self.start_value = []
        self.xlabels = []
        for i in range(2,len(data)):
            converted_data = data[i].split(",")
            try:
                self.start_value.append(float(converted_data[1]) / 10)
            except Exception as e:
                continue
            
            self.xlabels.append(converted_data[0])

        self.xsize = len(self.xlabels)
        self.lines.append(converted_data)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.start_value)
        self.ax.set_xticks(np.arange(0,self.xsize,self.xsize/10))
        self.ax.set_xticklabels(self.xlabels,fontsize=12)
        self.ax.title.set_text(str("Filter length: " + str(1) + "\nfilename: " + self.root.filename))
        self.ax.grid()
        self.canvas.draw()  
        self.file_loaded = True
start = MyPage()

button = tkinter.Button(master=start.root, text="Quit", command= start.quit)
button.pack(side=tkinter.BOTTOM)

button = tkinter.Button(master=start.root, text="LoadFile", command= start.LoadFile)
button.pack(side=tkinter.LEFT)

button = tkinter.Button(master=start.root, text="Increase", command=start.increase)
button.pack(side=tkinter.LEFT)
button = tkinter.Button(master=start.root, text="Decrease", command=start.decrease)
button.pack(side=tkinter.LEFT)
button = tkinter.Button(master=start.root, text="Gaussian", command=start.gaussianFilter)
button.pack(side=tkinter.LEFT)

sv = tkinter.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: start.customSized(sv))
e = tkinter.Entry(start.root, textvariable=sv,width=30)
e.insert(tkinter.END,"Custom Length")
e.pack(side=tkinter.LEFT)

sv2 = tkinter.StringVar()
sv2.trace("w", lambda name, index, mode, sv=sv2: start.customFilter(sv2))
e = tkinter.Entry(start.root, textvariable=sv2,width=30)
e.insert(tkinter.END,"Custom Filter, comma seperated")
e.pack(side=tkinter.LEFT)

tkinter.mainloop()




