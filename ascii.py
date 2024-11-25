import pygame as pg
import numpy as np
from numba import njit
import pygame.gfxdraw
import cv2

class ArtASCII:
    def __init__(self, path='photo/nya.jpg', font_size=12, screen_res=(800, 600)):
        pg.init()
        self.path = path
        self.screen_res = screen_res
        self.image = self.get_image()

        # Подгон изображения под размер экрана
        self.image = cv2.resize(self.image, self.screen_res, interpolation=cv2.INTER_AREA)

        self.RES = self.WIDTH, self.HEIGHT = self.screen_res
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def draw_converted_image(self):
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[y, x]  # Учитываем, что изображение уже масштабировано
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        gray_image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, self.screen_res, interpolation=cv2.INTER_AREA)
        cv2.imshow('photo', resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

class ArtASCIIColor:
    def __init__(self, path='photo/nya.jpg', font_size=12, screen_res=(800, 600),color_lvl=8):
        pg.init()
        self.path = path
        self.COLOR_LVL = color_lvl
        self.screen_res = screen_res
        self.image, self.gray_image = self.get_image()

        # Подгон изображения под размер экрана
        self.image = cv2.resize(self.image, self.screen_res, interpolation=cv2.INTER_AREA)

        self.RES = self.WIDTH, self.HEIGHT = self.screen_res
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = ' ixzao*#MW&8%B@$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def draw_converted_image(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[y, x]  # Учитываем, что изображение уже масштабировано
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[y,x])
                    self.surface.blit(self.PALETTE[char][color], (x, y))
    def create_palette(self):
        colors, color_coeff = np.linspace(0,255,num = self.COLOR_LVL, dtype=int,retstep = True)
        color_palette = [np.array([r,g,b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        #transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(self.cv2_image,cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2GRAY)
        return image, gray_image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, self.screen_res, interpolation=cv2.INTER_AREA)
        cv2.imshow('photo', resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()