import pygame as pg
import numpy as np
from numba import njit
import pygame.gfxdraw
import cv2


class ArtPixelColor:
    def __init__(self, path='photo/nya.png', pixel_size=7, color_lvl=8, screen_res=(800,600)):
        pg.init()
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.screen_res = screen_res
        self.image = self.get_image()
        self.image = cv2.resize(self.image, self.screen_res, interpolation=cv2.INTER_AREA)

        self.RES = self.WIDTH, self.HEIGHT = self.screen_res
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.transpose(frame)


    def draw_converted_image(self):
        color_indices = self.image // self.COLOR_COEFF
        for x in range (0, self.WIDTH, self.PIXEL_SIZE):
            for y in range (0, self.HEIGHT, self.PIXEL_SIZE):
                color_key = tuple(color_indices[y,x])
                if sum(color_key):
                    color = self.PALETTE[color_key]
                    pygame.gfxdraw.box(self.surface, (y, x, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

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

class ArtPixel:
    def __init__(self, path='photo/nya.png', pixel_size=7, screen_res=(800, 600)):
        pg.init()
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.screen_res = screen_res
        self.image = self.get_image()
        self.image = cv2.resize(self.image, self.screen_res, interpolation=cv2.INTER_AREA)

        self.RES = self.WIDTH, self.HEIGHT = self.screen_res
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def apply_gray_filter(self):
        """Применяет серый фильтр к изображению."""
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # Конвертируем изображение обратно в 3 канала для рисования.
        gray_image_rgb = cv2.merge([gray_image] * 3)
        return gray_image_rgb

    def draw_converted_image(self):
        """Рисует изображение с наложенным серым фильтром."""
        gray_image = self.apply_gray_filter()
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                # Берём цвет пикселя.
                r, g, b = gray_image[y, x]
                pygame.gfxdraw.box(self.surface, (y, x, self.PIXEL_SIZE, self.PIXEL_SIZE), (r, g, b))

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

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
