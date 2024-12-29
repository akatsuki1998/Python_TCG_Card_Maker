from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import ImgLoader as imgLoad
import item_config as item
from tkinter import messagebox
import ComboboxTip as cbTip
import cardData
import cardImgWindow
class OperateWindows():
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap(imgLoad.resource_path('icon/icon.ico'))
        self.master.title('My TCG Maker')
        self.master.geometry('500x360')
        self.widgets = []  # 用來存儲所有控件的列表
        self.setup_ui()
    def setup_ui(self):

        self.name_label = ttk.Label(self.master, text='輸入卡片名稱:')
        self.name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.name_str = StringVar()
        self.name_input = Entry(self.master, width=30, textvariable=self.name_str)
        self.name_input.grid(row=1, column=0, sticky="we", padx=5)
        self.name_input.bind("<KeyRelease>", self.get_name)

        self.power_label = ttk.Label(self.master, text='Power:')
        self.power_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.power_selector = self.create_combobox(3, item.power_selector_items)
        self.power_selector.grid(row=1, column=1, sticky="we", padx=5)
        self.power_selector.bind("<<ComboboxSelected>>", self.get_power)

        self.level_label = ttk.Label(self.master, text='Level:')
        self.level_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        self.level_selector = self.create_combobox(3, item.level_selector_items)
        self.level_selector.grid(row=1, column=2, sticky="we", padx=5)
        self.level_selector.bind("<<ComboboxSelected>>", self.get_level)

        self.feature_label = ttk.Label(self.master, text='輸入特徵:')
        self.feature_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.feature_str = StringVar()
        self.feature_input = Entry(self.master, width=20, textvariable=self.feature_str)
        self.feature_input.grid(row=3, column=0, sticky="we", padx=5)
        self.feature_input.bind("<KeyRelease>", self.get_feature)

        self.type_label = ttk.Label(self.master, text='卡片種類:')
        self.type_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.type_selector = self.create_combobox(10, item.type_selector_items)
        self.type_selector.grid(row=3, column=1, sticky="we", padx=5)
        self.type_selector.bind("<<ComboboxSelected>>",  lambda event: (self.get_type(event), self.set_power_selector_off(event)))

        self.class_label = ttk.Label(self.master, text='職業:')
        self.class_label.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.class_selcctor = self.create_combobox(5, item.class_selector_items)
        self.class_selcctor.grid(row=3, column=2, sticky="we", padx=5)
        self.class_selcctor.bind("<<ComboboxSelected>>", self.get_class)

        self.effect_label = ttk.Label(self.master, text='新增效果 (最多只能4個能力):')
        self.effect_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.add_effect_btn = Button(text="+", command=lambda : self.add_widgets(False, None))
        self.add_effect_btn.grid(row=4, column=1, columnspan=1, sticky="we", padx=5)

        self.sub_effect_btn = Button(text="-", command=self.sub_widgets)
        self.sub_effect_btn.grid(row=4, column=2, columnspan=1, sticky="we", padx=5)

        self.save_card = ttk.Button(self.master, text='儲存', command=self.save)
        self.save_card.grid(row=6, column=2, columnspan=1, sticky="we", padx=5)

        self.select_image = ttk.Button(self.master, text='選擇照片', command=self.select_img)
        self.select_image.grid(row=7, column=2, columnspan=1, sticky="we", padx=5)

        self.import_thsc = ttk.Button(self.master, text='開啟舊檔',command=self.select_thsc)
        self.import_thsc.grid(row=8, column=2, columnspan=1, sticky="we", padx=5)

        # 配置行和列的權重，使元件隨窗口大小調整
        for i in range(9):  # 行
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(3):  # 列
            self.master.grid_columnconfigure(i, weight=1)
    def create_combobox(self, width, value):
        com = ttk.Combobox(self.master,  textvariable=StringVar(), width=width)
        com['value'] = (value)
        com.current(0)
        return com
    def add_widgets(self, isread, card_effect):
        # 計算新組件的位置
        if len(self.widgets) >= 4:
            return

        rows = 5 + len(self.widgets)

        frame = tk.Frame(self.master)
        frame.grid(row=rows, column=0, columnspan=2, sticky="we", padx=5)

        # 創建Label
        effext_label = tk.Label(frame, text=f"效果 {len(self.widgets) + 1}")
        effext_label.pack(side=tk.LEFT, padx=1)

        # 創建Combobox
        all_effect = item.basic_ablities_selector_items + item.spec_abilites_selector_items
        effect_type_selector = ttk.Combobox(frame, width=8, values=all_effect)
        effect_type_selector.pack(side=tk.LEFT, padx=5)
        effect_type_selector.bind("<<ComboboxSelected>>", lambda event, cb=effect_type_selector, f=frame: (
        self.on_combobox_select(event, cb, f), self.on_widget_change(event, cb, f)))

        if isread:
            effect_type_selector.set(card_effect.effect)

        tips = cbTip.ComboboxTip(effect_type_selector)
        for index, selector_item in enumerate(all_effect):
            tips.add_tooltip(index, item.ablities_des_dict[selector_item])

        # 創建Entry（文字輸入框）
        effect_text = tk.Entry(frame, width=40)
        effect_text.pack(side=tk.LEFT, padx=5)
        effect_text.bind("<KeyRelease>", lambda event, e=effect_text, f=frame: self.on_widget_change(event, e, f))
        if isread:
            effect_text.insert(END, card_effect.effect_text)

        # 將所有新生成的組件添加到列表中
        self.widgets.append(
            {"frame": frame, "combobox": effect_type_selector, "entry": effect_text, "label": effext_label, "index": len(self.widgets)})
    def sub_widgets(self):
        if self.widgets:

            widgets_num = len(self.widgets)
            # 獲取最後一組控件
            last_widget = self.widgets.pop()
            # 從界面中移除該框架
            last_widget['frame'].pack_forget()
            # 如果需要，完全銷毀該框架
            last_widget['frame'].destroy()

            # 獲取字典的鍵列表
            keys = list(cardData.effect_items.keys())
            item_num = len(keys)

            # 刪除最後一個鍵對應的資料
            if keys and (widgets_num == item_num):  # 確保字典不為空
                del cardData.effect_items[keys[-1]]
    def on_combobox_select(self, event, cb, frame):
        if cb.get() in item.basic_ablities_selector_items:
            # 找到相應的Entry並清空它
            entry = next(widget['entry'] for widget in self.widgets if widget['frame'] == frame)
            entry.delete(0, tk.END)
            entry.config(state="disabled")
        else:
            # 如果選擇了其他選項，恢復Entry的輸入狀態
            entry = next(widget['entry'] for widget in self.widgets if widget['frame'] == frame)
            entry.config(state="normal")
    def on_widget_change(self, event, widget, frame):
        # 找到對應的Combobox和Entry
        widget_info = next(w for w in self.widgets if w['frame'] == frame)
        effect = widget_info['combobox']
        effect_text = widget_info['entry']
        index = widget_info['index'] + 1  # 組合的順序從1開始
        data = cardData.card_effect(effect.get(), effect_text.get())

        if index in cardData.effect_items.keys():
            cardData.effect_items[index].effect = data.effect
            cardData.effect_items[index].effect_text = data.effect_text

        else:
            cardData.effect_items[index] = data
    def save(self):
        disallowed_chars = set('@#$%^&*()+=[]{}|;:,.<>?')

        if cardData.name != "" and not any(char in disallowed_chars for char in cardData.name):
            cardData.cardInfo.save_card()
        else:
            messagebox.showinfo("錯誤", "不可為空值，不可出現以下符號(@#$%^&*()+=[]{}|;:,.<>?)")
    def select_img(self):
        try:
            file_path = filedialog.askopenfilename()
            cardData.imgSrc = file_path
            cardData.cardInfo.set_card_image(file_path)
            cardData.isimg = True
        except Exception as e:
            cardData.isimg = False
            messagebox.showinfo("存取圖片失敗", "發生錯誤: " + str(e))
    def select_thsc(self):
        try:
            # 打開文件選擇對話框
            file_path = filedialog.askopenfilename(
                filetypes=[("THSC files", "*.thsc"), ("All files", "*.*")],
                title="選擇一個THSC文件"
            )
            # 檢查選擇的文件是否存在且是否為.thsc格式
            if file_path:
                # 清空
                for i in reversed(range(len(self.widgets))):
                    last_widget = self.widgets.pop()
                    # 從界面中移除該框架
                    last_widget['frame'].pack_forget()
                    # 如果需要，完全銷毀該框架
                    last_widget['frame'].destroy()

                cardData.cardInfo.process_file(file_path)
                self.set_card_value()
        except Exception as e:
            messagebox.showinfo("卡片效果讀取錯誤", "發生錯誤 :" + str(e))
    def get_name(self, event):
        value = event.widget.get()
        try:
            cardData.name = value
        except ValueError:
            cardData.name = "輸入內容有錯"
    def get_power(self, event):
        value = event.widget.get()
        try:
            cardData.power = value
        except ValueError:
            cardData.power = "輸入內容有錯"
    def get_level(self,event):
        value = event.widget.get()
        try:
            cardData.level = value
        except ValueError:
            cardData.level = "輸入內容有錯"
    def get_feature(self, event):
        value = event.widget.get()
        try:
            cardData.feature = value
        except ValueError:
            cardData.feature = "輸入內容有錯"
    def get_type(self, event):
        value = event.widget.get()
        try:
            cardData.card_type = value
        except ValueError:
            cardData.card_type = "輸入內容有錯"
    def get_class(self, event):
        value = event.widget.get()
        try:
            cardData.cardClass = value
        except ValueError:
            cardData.cardClass = "輸入內容有錯"
    def set_card_value(self):
        self.name_input.delete(0, tk.END)
        self.name_input.insert(END, cardData.name)
        self.power_selector.set(cardData.power)
        self.level_selector.set(cardData.level)
        self.feature_input.delete(0, tk.END)
        self.feature_input.insert(END, cardData.feature)
        self.type_selector.set(cardData.card_type)
        self.class_selcctor.set(cardData.cardClass)

        for key, value in cardData.effect_items.items():
            self.add_widgets(True, value)

    def set_power_selector_off(self, event):
        current_type = self.type_selector.get()
        if current_type != "從者":
            self.power_selector.set("No Power")
            self.power_selector.config(state="disable")
        else:
            self.power_selector.set(cardData.power)
            self.power_selector.config(state="normal")

def window():
    root = tk.Tk()
    OperateWindows(root)
    root.mainloop()

def window2():
    card_window = cardImgWindow.CardWindow(348, 476)
    card_window.run()

if __name__ == '__main__':
    thread1 = Thread(target=window)
    thread2 = Thread(target=window2)
    threads = [thread1, thread2]
    for t in threads:
        t.start()
