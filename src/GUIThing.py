import tkinter as tk
import os

def doNothing():
    pass

def makeWindow(title="ex. Title", size=None, minx=100, miny=100, maxx=1920, maxy=1080):
    window = tk.Tk()

    window.title=title
    if size is not None:
        window.geometry=size

    window.minsize(minx, miny)
    window.maxsize(maxx, maxy)

    return window

def makeGridEx(parent):
    # parent.grid()

    label = tk.Label(parent, anchor="center", bg="green")
    label.grid(column=0, row=0, sticky='NSEW')

    label2 = tk.Label(parent, anchor="center", bg="black")
    label2.grid(column=1, row=0, sticky='NSEW')

    label3 = tk.Label(parent, anchor="center", bg="red")
    label3.grid(column=2, row=0, sticky='NSEW')

    label4 = tk.Label(parent, anchor="center", bg="purple")
    label4.grid(column=0, row=1, sticky='NSEW')

    label5 = tk.Label(parent, anchor="center", bg="blue")
    label5.grid(column=1, row=1, sticky='NSEW')

    label6 = tk.Label(parent, anchor="center", bg="yellow")
    label6.grid(column=2, row=1, sticky='NSEW')

    parent.grid_columnconfigure(0, pad=50)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=1)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_rowconfigure(1, weight=1)

def makePanels(parent):
    top = tk.Label(parent, anchor="center", bg="gray")
    top.grid(column=0, row=0, sticky='NSEW')

    bottom = tk.Label(parent, anchor="center", bg="black")
    bottom.grid(column=0, row=1, sticky='NSEW')

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_rowconfigure(1, pad=10)

    # bottom subgrid
    btn = tk.Button(bottom, text="helloo", anchor="center")
    bottom.grid_columnconfigure(0, weight=1)
    bottom.grid_rowconfigure(0, weight=1)
    btn.grid(column=0, row=0, sticky='NSEW')


window = makeWindow()

#makeGridEx(window)
makePanels(window)

#frame = tk.Frame(window, bg="gray")
#frame.place()
#frame.pack(expand=True)

#canvas = tk.Canvas(window, bg="#263D42")
#canvas.pack()


#openFile = tk.Button(window, text="open File", padx=10, pady=5, fg="black", bg="gray", command=doNothing)
#openFile.pack()

window.mainloop()