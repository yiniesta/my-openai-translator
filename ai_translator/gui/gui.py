import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE

class GUI:
    def __init__(self, model, translator):
        self.model = model
        self.translator = translator
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Translation GUI')
        self.font = pygame.font.Font(None, 30)
        self.input_text = ""
        self.selected_language = "English"

    def display_text(self, text, position):
        rendered_text = self.font.render(text, True, pygame.Color('black'))
        self.screen.blit(rendered_text, position)

    def run(self):
        # 初始化GUI界面

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        # 用户按下回车键进行翻译
                        translated_text = self.translator.translate_text(self.input_text, self.selected_language)
                        print("Translation:", translated_text)  # 在控制台输出翻译结果
                        # 在GUI界面上显示翻译结果
                        self.display_text("Translation: " + translated_text, (50, 150))
                        pygame.display.update()
                    elif event.key == K_BACKSPACE:
                        # 用户按下退格键，删除最后一个字符
                        self.input_text = self.input_text[:-1]
                    else:
                        # 将用户输入的字符添加到输入文本中
                        self.input_text += event.unicode

            # 绘制GUI界面
            self.screen.fill(pygame.Color('white'))

            # 绘制语言选择框
            pygame.draw.rect(self.screen, pygame.Color('lightgray'), (50, 50, 200, 50))
            self.display_text("Selected Language: " + self.selected_language, (60, 60))

            # 绘制输入文本框
            pygame.draw.rect(self.screen, pygame.Color('lightgray'), (50, 100, 700, 50))
            self.display_text("Input Text: " + self.input_text, (60, 110))

            # 绘制翻译按钮
            pygame.draw.rect(self.screen, pygame.Color('lightblue'), (50, 200, 100, 50))
            self.display_text("Translate", (60, 210))

            pygame.display.update()

            # 添加其他GUI的交互逻辑和响应事件
