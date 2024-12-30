import pygame
import os
import sys
from tkinter import messagebox
import cardData
import item_config
class CardWindow:
    def __init__(self, x, y):
        pygame.init()
        self.x = x
        self.y = y
        self.screen = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption('Card Maker')
        self.icon = pygame.image.load('icon/icon.png')
        pygame.display.set_icon(self.icon)

        # Load assets
        self.card_bg_items = {}
        for item in item_config.class_selector_items:
            trans_item = item_config.zh_eng[item]
            card_bg = pygame.image.load('assets/card_bg/{}.png'.format(trans_item)).convert()
            card_bg.set_colorkey((0, 0, 0))
            self.card_bg_items[trans_item] = card_bg

        self.card_power_icon = pygame.image.load('assets/card_icon/type/Power.png').convert_alpha()
        self.card_type_icon_items = {}

        for item in item_config.type_selector_items:
            trans_item = item_config.zh_eng[item]
            card_type = pygame.image.load('assets/card_icon/type/{}.png'.format(trans_item)).convert()
            card_type.set_colorkey((0, 0, 0))
            self.card_type_icon_items[trans_item] = card_type

        self.card_effect_icon_items = self.load_effect_icon("assets/card_icon/effect")
        # Font setup
        pygame.font.init()
        self.card_font = 'assets/fonts/R-PMingLiU-TW-2.ttf'

        # Initial state
        self.posx = cardData.posx
        self.posy = cardData.posy
        self.imgx = 0
        self.imgy = 0
        self.isimg = 0
        self.card_img = None
        self.effect_text = ''
        self.scale = cardData.cscale

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.handle_key_press(keys)
            self.isimg = cardData.isimg
            self.update_screen()
    def handle_key_press(self, keys):
        # Handle image movement
        if keys[pygame.K_RIGHT]:
            self.posx += 1
            self.update_img_size()
        if keys[pygame.K_LEFT]:
            self.posx -= 1
            self.update_img_size()
        if keys[pygame.K_UP]:
            self.posy -= 1
            self.update_img_size()
        if keys[pygame.K_DOWN]:
            self.posy += 1
            self.update_img_size()

        # Handle image scaling
        if cardData.cardImg != None:
            if keys[pygame.K_w] and self.scale <= 2.01:
                self.scale += 0.005
                self.update_img_size()

            if keys[pygame.K_s] and self.scale >= 0.11:
                self.scale -= 0.005
                self.update_img_size()
    def update_screen(self):
        self.screen.fill((0, 0, 0))
        cardData.card_screen = self.screen
        # Draw card image
        if self.isimg:
            if cardData.cardImg != None:
                self.posx = cardData.posx
                self.posy = cardData.posy
                self.scale = cardData.cscale
                self.card_img = pygame.transform.smoothscale(cardData.cardImg, (
                int(cardData.cwidth * self.scale), int(cardData.cheight * self.scale)))
                self.screen.blit(self.card_img, (self.posx, self.posy))



        # Draw background
        class_eng = item_config.zh_eng[cardData.cardClass]
        self.screen.blit(self.card_bg_items[class_eng], (0, 0))

        # Draw name
        name_font = pygame.font.Font(self.card_font, 20)
        name_text = name_font.render(cardData.name, True, (0, 0, 0))
        text_rect = name_text.get_rect(center=(self.x / 2, self.y / 2 - 205))
        self.screen.blit(name_text, text_rect)

        # Draw effect text
        rule_font = pygame.font.Font(self.card_font, 15)
        lines = self.process_data(cardData.effect_items)
        for i, line in enumerate(lines):
            text_surface = rule_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (40, 350 + i * 20))

        # Draw type text
        type_font = pygame.font.Font(self.card_font, 20)
        type_text = type_font.render(cardData.card_type, True, (0, 0, 0))
        self.screen.blit(type_text, (55, 320))

        # Draw type icon
        if cardData.card_type == '從者':
            power_icon_img = pygame.transform.smoothscale(self.card_power_icon, (120, 40))
            self.screen.blit(power_icon_img, (210, 410))

            power_font = pygame.font.SysFont('Arial Bold', 50)
            power_text = power_font.render(str(cardData.power), True, (255, 255, 255))
            self.screen.blit(power_text, (255, 415))

        type_eng = item_config.zh_eng[cardData.card_type]
        icon_img = pygame.transform.smoothscale(self.card_type_icon_items[type_eng], (31, 31))
        self.screen.blit(icon_img, (19, 315))

        #draw feature text
        feature_font = pygame.font.Font(self.card_font, 17)
        feature_text = feature_font.render('--'+cardData.feature, True, (0, 0, 0))
        self.screen.blit(feature_text, (95, 322))

        # Draw level
        level_font = pygame.font.SysFont('Arial Bold', 50)
        text = level_font.render(str(cardData.level), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x / 8-2, self.y / 8-26))
        self.screen.blit(text, text_rect)

        level_font = pygame.font.SysFont('Arial Bold', 25)
        level_text = level_font.render('Level', True, (0, 0, 0))

        offset = 1  # 外框的厚度
        # 繪製外框（黑色）
        for offset_x in range(-offset, offset + 1):
            for offset_y in range(-offset, offset + 1):
                self.screen.blit(level_font.render("Level", True, (255, 255, 255)),
                            (20 + offset_x, 42 + offset_y))

        self.screen.blit(level_text, (20, 42))

        pygame.display.flip()
    def process_data(self, data):
        """
        處理字典數據，將其轉換為list[str]格式，並合併相應的條目。

        :param data: 原始的字典數據
        :return: 處理後的列表，包含字符串格式的條目
        """
        result = []
        last_item_empty = False

        for key in sorted(data.keys()):  # 確保按鍵的順序處理
            current_item = data[key]
            effect = current_item.effect
            spec_effect_text = ""
            if effect != "其他":
                spec_effect_text = f"【{effect}】"
            if last_item_empty and not current_item.effect_text:
                # 檢查前一個條目的最後一個字符是否是逗號
                if result[-1].endswith(','):
                    result[-1] = result[-1][:-1] + "," + spec_effect_text
                else:
                    result[-1] += "," + spec_effect_text
                last_item_empty = True
            else:
                # 如果不是合併情況，則直接添加
                symbol = ":"
                max_line = 20
                if (key == 1 and not current_item.effect_text) or effect == "其他":
                    symbol = ""
                if len(current_item.effect_text) <= max_line:
                    result.append(f"-{spec_effect_text}{symbol} {current_item.effect_text}")
                else:

                    text = current_item.effect_text
                    effect_text_parts = []
                    start = 0
                    # 第一次切割15個字符
                    if len(text) >= 15:
                        effect_text_parts.append(text[start:start + 15])
                        start += 15

                    # 之後的每次切割20個字符
                    for i in range(start, len(text), max_line):
                        effect_text_parts.append(text[i:i + max_line])

                    result.append(f"-【{effect}】{symbol} {effect_text_parts[0]}")
                    # 如果split_list至少有兩個元素
                    if len(effect_text_parts) >= 2:
                        # 使用extend將split_list從第二個元素開始加入到new_list
                        result.extend(effect_text_parts[1:])

                last_item_empty = not bool(current_item.effect_text)


        return result
    def load_effect_icon(self, folder_path):
        # 檢查資料夾是否存在
        if not os.path.isdir(folder_path):
            messagebox.showerror("錯誤", "讀取資料失敗！")
            raise ValueError(f"The specified folder '{folder_path}' does not exist.")

        # 獲取資料夾中的所有圖片檔案
        image_files = [f for f in os.listdir(folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        # 使用字典來存儲圖片
        images = {}

        for image_file in image_files:
            file_path = os.path.join(folder_path, image_file)
            try:
                # 使用pygame載入圖片
                image = pygame.image.load(file_path)
                key = image_file.split(".png")[0]
                images[key] = image
            except pygame.error as e:
                messagebox.showerror("錯誤", "讀取資料失敗！")


        return images
    def update_img_size(self):
        cardData.posy = self.posy
        cardData.posx = self.posx
        cardData.cscale = self.scale