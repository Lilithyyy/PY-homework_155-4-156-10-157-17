import tkinter as tk #import needed libs
import random

column_width = 20
amount = 15
gap = 5
fps = 30
interval = int(1000 / fps)  #set fps
height_change_interval = [-3, 3]

w = amount * column_width + (amount * gap * 2) #width based on amount of columns
h = 150

root = tk.Tk() #create main window
root.title("Music Equalizer")
root.resizable(False, False)
root.geometry(f"{w}x{h}")
#^ set window properties

c = tk.Canvas(root, width=w,height=h, bg="black") #create canvasw
c.pack()

heights = amount * [0,]
print(heights)

while True: #run forever loop
 
    c.delete("all")

    for i in range(amount):
        x0 = i * (column_width + gap * 2) + gap #divide columns with gaps
        y0 = h - 20
        
        heights[i] = abs(heights[i] + random.randrange(height_change_interval[0], height_change_interval[1])) #change height randomly

        if heights[i] > h - 20:
            heights[i] = h - 20

        c.create_rectangle(x0, y0, x0 + column_width, y0 - heights[i], fill="lime", outline="")
        c.create_text(x0 + column_width / 2, h - 10, text=str(heights[i]), fill="lime", font=("Arial", 8), anchor="center")

    c.after(interval)
    c.update()