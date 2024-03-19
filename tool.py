import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
root = tk.Tk()  # 创建一个Tk实例
a=ttk.Frame(root)
a.grid(row=50,column=100)
available_fonts = tk.font.families(root)[10:]
print(available_fonts)
c=10
d=0
for font in available_fonts:
    f=tkFont.Font(family=f"{font}", size=10)
    b=ttk.Label(a,text=f'Aa李{font}',font=f)
    b.grid(row=c,column=d,padx=20,pady=10, columnspan=1)
    if c==15:
        c=0
        d+=1
    else:
        c+=1
a.pack()

root.geometry("1000x1000")
root.mainloop()