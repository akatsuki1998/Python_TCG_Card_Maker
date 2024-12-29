# 靜態變數
import pygame
import os
import ast
from tkinter import messagebox

power = 10
name = ''
level = 0
card_type = '從者'
feature = 'None'
effect_items = {}
imgSrc = ''
cardClass = '創造者'
isimg = False
cardImg = None
card_screen = None
cwidth = 0
cheight = 0
class cardInfo:
    @staticmethod
    def set_card_image(file_path):
        global cardImg, isimg, cwidth, cheight
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                cardImg = pygame.image.load(file_path).convert()
                cwidth, cheight = cardImg.get_size()
                isimg = True
            except pygame.error:
                print(f"無法載入圖像文件: {file_path}")
                isimg = False

    @staticmethod
    def save_card():
        global card_screen
        try:
            img_save_Path = './output/images/'
            if not os.path.exists(img_save_Path):
                os.makedirs(img_save_Path)
            txt_save_path = './output/thsc/'
            if not os.path.exists(txt_save_path):
                os.makedirs(txt_save_path)

            # Save the image
            pygame.image.save(card_screen, os.path.join(img_save_Path, f"{name}.png"))

            # Save the text data
            with open(os.path.join(txt_save_path, f"{name}.thsc"), 'w', encoding="utf-8") as f:
                f.write(f"name :{name}\n")
                f.write(f"power : {power}\n")
                f.write(f"level : {level}\n")
                f.write(f"type : {card_type}\n")
                f.write(f"feature : {feature}\n")
                f.write(f"cardClass : {cardClass}\n")
                f.write(f"imgSrc :{imgSrc}\n")
                f.write(f"effect_items : {cardInfo.effect_items_to_str(effect_items)}\n")
                f.write(f"cwidth :{cwidth}\n")
                f.write(f"cheight :{cheight}\n")

            messagebox.showinfo("保存成功", "數據已成功保存！")
        except Exception as e:
            messagebox.showinfo("保存失敗", f"發生錯誤: {str(e)}")

    @staticmethod
    def process_file(file_path):
        if file_path.lower().endswith('.thsc'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    cardInfo.read_data_from_file(file)
            except UnicodeDecodeError:
                messagebox.showinfo("錯誤", "無法使用UTF-8編碼讀取文件，請確認文件是否為文本文件或使用其他編碼。。")
        else:
            messagebox.showinfo("錯誤", "你選擇的文件不是THSC格式。")
    @staticmethod
    def read_data_from_file(file):
        global name, power, level, card_type, feature, cardClass, imgSrc, effect_items, cwidth, cheight
        for line in file:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # 根據鍵名將值分配給對應的變數
                if key == "name":
                    name = value
                elif key == "power":
                    power = value
                elif key == "level":
                    level = value
                elif key == "type":
                    card_type = value
                elif key == "feature":
                    feature = value
                elif key == "cardClass":
                    cardClass = value
                elif key == "imgSrc":
                    imgSrc = value
                    cardInfo.set_card_image(imgSrc)
                elif key == "effect_items":
                    parsed_dict = ast.literal_eval(value)
                    effect_items = {k: card_effect.from_dict(v) for k, v in parsed_dict.items()}
                elif key == "cwidth":
                    cwidth = float(value)
                elif key == "cheight":
                    cheight = float(value)
                else:
                    messagebox.showinfo("錯誤", f"未識別的鍵: {key}")

    @staticmethod
    def effect_items_to_str(effect_items):
        parsed_dict = {k: v.to_dict() for k, v in effect_items.items()}

        # 將轉換後的字典轉換為字符串
        result_str = cardInfo.dict_to_str(parsed_dict)

        return result_str

    @staticmethod
    def dict_to_str(d):
    # 將字典轉換為字符串
        return "{" + ", ".join(f"{k}: {v}" for k, v in d.items()) + "}"

class card_effect:
    def __init__(self, effect, effect_text):
        self.effect = effect
        self.effect_text = effect_text

    def to_dict(self):
        return {"effect": self.effect, "effect_text": self.effect_text}

    @classmethod
    def from_dict(cls, data):
        return cls(effect=data['effect'], effect_text=data['effect_text'])
