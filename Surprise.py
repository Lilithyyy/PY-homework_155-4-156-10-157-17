import tkinter as tk

w = 300
h = 100

root = tk.Tk()
root.title("Surprise")
root.geometry(f"{w}x{h}")
root.resizable(False, False)

def on_close():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

c=tk.Canvas(root, width=w, height=h, bg="#B09BBD")
c.pack()

xfile = open("x.txt", "r")
yfile = open("y.txt", "r")

coords = []
steps = 0

for line in xfile:
    coords.append((int(line.rstrip()), int(yfile.readline().rstrip())))
    steps += 1

xfile.close()
yfile.close()

print(coords)
print(steps)
print(len(coords))

def DrawCircle(x,y):
    c.create_oval(x-5, y-5, x+5, y+5, fill="white", outline="")

for i in range(steps):
    c.after(500, DrawCircle(coords[i][0], coords[i][1]))
    c.update()

root.mainloop()