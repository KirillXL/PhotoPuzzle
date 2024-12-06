import pygame as pg
import os



class Interface:
    def __init__(self,path = "photo" ,screen_res = (800,600)):
        # Инициализация Pygame
        pg.init()
        self.PATH = path
        # Настройки окна
        self.screen_res = screen_res
        self.RES = self.WIDTH, self.HEIGHT = screen_res
        self.surface = pg.display.set_mode(self.RES)

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        # Шрифт
        self.font = pg.font.Font(None, 36)

        self.clock = pg.time.Clock()

    # Функция отображения текста
    def render_text(self, text, x, y,font = None, color = (0,0,0), center=True):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2
        self.surface.blit(text_surface, (x, y))

    # Основной цикл
    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.select_event()
            pg.display.flip()
            self.clock.tick(30)

    def select_event(self):
        raise NotImplementedError("Этот метод должен быть реализован в дочернем классе")



class PickPicture(Interface):
    def __init__(self,path = "photo",screen_res = (800,600)):
        super().__init__(path,screen_res)



    def select_event(self):
        pg.display.set_caption("Выбор картинки")
        # Список изображений
        try:
            images = [os.path.join(self.PATH, img) for img in os.listdir(self.PATH)
                      if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        except FileNotFoundError:
            print(f"Папка {self.PATH} не найдена!")
            return None

        if not images:
            print(f"В папке {self.PATH} нет подходящих изображений!")
            return

        running = True
        selected_image = None

        while running:
            self.surface.fill(self.WHITE)

            # Отображение списка изображений
            for i, img_path in enumerate(images):
                rect = pg.Rect(50, 50 + i * 50, 700, 50)
                pg.draw.rect(self.surface, self.GRAY, rect)
                pg.draw.rect(self.surface, self.BLACK, rect, 2)
                self.render_text(os.path.basename(img_path), rect.centerx, rect.centery)

            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
                    mouse_x, mouse_y = event.pos
                    for i, img_path in enumerate(images):
                        rect = pg.Rect(50, 50 + i * 50, 700, 50)
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_image = img_path
                            running = False
            pg.display.flip()
            self.clock.tick(30)



        return selected_image

class PickArt(Interface):
    def __init__(self, path="photo", screen_res=(800, 600)):
        super().__init__(path, screen_res)

    def select_event(self):
        pg.display.set_caption("Выбор cтиля")
        # Список изображений

        art_array = ['ASCII','ASCII Color', 'PIXEL','PIXEL Color']

        running = True
        select_art = None

        while running:
            self.surface.fill(self.WHITE)

            # Отображение списка изображений
            for i, name_art in enumerate(art_array):
                rect = pg.Rect(50, 50 + i * 50, 700, 50)
                pg.draw.rect(self.surface, self.GRAY, rect)
                pg.draw.rect(self.surface, self.BLACK, rect, 2)
                self.render_text(name_art, rect.centerx, rect.centery)

            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
                    mouse_x, mouse_y = event.pos
                    for i, name_art in enumerate(art_array):
                        rect = pg.Rect(50, 50 + i * 50, 700, 50)
                        if rect.collidepoint(mouse_x, mouse_y):
                            select_art = name_art
                            running = False
            pg.display.flip()
            self.clock.tick(30)

        return select_art