import tkinter as tk
from tkinter import ttk

class SetComboboxExample:
    def __init__(self, master):
        self.master = master
        self.master.title("Set Combobox Example")
        self.setup_ui()

    def setup_ui(self):
        # 創建Combobox小部件
        self.combobox = ttk.Combobox(self.master, values=["Option 1", "Option 2", "Option 3"])
        self.combobox.grid(row=0, column=0, padx=5, pady=5)
        self.combobox.set("Option 1")  # 設置初始值

        # 創建按鈕並綁定事件
        self.set_button = tk.Button(self.master, text="Set to Option 3", command=self.set_combobox)
        self.set_button.grid(row=1, column=0, padx=5, pady=5)

        # 創建一個標籤來顯示當前選擇
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=2, column=0, padx=5, pady=5)

    def set_combobox(self):
        # 設置Combobox的選項為 "Option 3"
        self.AA()  # 呼叫AA函數

        # 更新標籤顯示
        self.result_label.config(text=f"Combobox has been set to: {self.combobox.get()}")

    def AA(self):
        # 在這裡更改Combobox的選項內容
        self.combobox.set("Option 3")

root = tk.Tk()
app = SetComboboxExample(root)
root.mainloop()
