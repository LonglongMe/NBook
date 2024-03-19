import tkinter as tk  
from tkinter import ttk  
from tkinter import font as tkFont
import ctypes

#ctypes.windll.shcore.SetProcessDpiAwareness(1)
#ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)


from tkintertable import TableCanvas  

 
  
import tkinter as tk  
from tkinter import ttk  
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 创建主窗口  
root = tk.Tk()  
root.title("Ttk Listbox 示例")  
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")
root.tk.call('tk', 'scaling', ScaleFactor/80)  
# 创建一个Frame来放置Listbox  
frame = ttk.Frame(root, padding=1)  
frame.pack(fill=tk.BOTH, expand=True)  
a=ttk.Label(frame,width=10,text="-------------------")
a.grid(row=0,column=1)
for i in range(1,100):
    a=ttk.Separator(frame)
    a.grid(row=i,column=1,pady=5,padx=0)

  
# 运行Tkinter主循环  
root.mainloop()



"""
# 创建 Tkinter 窗口  
root = tk.Tk()  
root.title("TkinterTable 示例")  
  
# 创建表格对象  
table = TableCanvas(root)  
  
# 定义表格数据和列标题  
data = [  
    ['姓名', '年龄', '城市'],  
    ['Alice', 25, 'New York'],  
    ['Bob', 32, 'Paris'],  
    ['Charlie', 18, 'London'],  
]  
  
# 将数据添加到表格中  
table.createTable(data, showtoolbar=False, showstatusbar=False)  
  
# 配置表格的样式（可选）  
table.configure(stretch='all', selectmode='browse')  
  
# 将表格添加到窗口中  
table.pack(fill='both', expand=True)  
  
#root.tk.call('tk', 'scaling', ScaleFactor/70)# 运行 Tkinter 主循环  
root.mainloop()"""

"""        self.treeview = ttk.Treeview(
            self.window.lp,
            #selectmode="browse",
            show="headings",
            columns=("meaning","egsentence"),
            height=10,
        )
        #self.treeview.grid(row=1,column=1)
        #self.treeview.pack(expand=True, fill="both") 
        # Treeview columns
        self.treeview.column("meaning", anchor="w", width=120)
        self.treeview.column("egsentence", anchor="w", width=200)
        self.treeview.heading("meaning", text="meaning")  
        self.treeview.heading("egsentence", text="egsentence") 
        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", ("Item 1", "Value 1")),
            (1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
            ("", 6, "Parent", ("Item 2", "Value 2")),
            (6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14, "Parent", ("Item 3", "Value 3")),
            (14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
            (14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
            (14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
            (14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19, "Parent", ("Item 4", "Value 4")),
            (19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
            (19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
            (21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
            (21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
            (21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
            (19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
        ]

        # Insert treeview data
        #for item in treeview_data:
         #   self.treeview.insert("", "end", value=(item[1],item[2]))
        self.treeview.insert("", "end", values=("Value 1", "Value 2"))  
        self.treeview.insert("", "end", values=("Value 4", "Value 5")) 
        self.treeview.pack(expand=True, fill="both") 
"""
        # Select and scroll