import pygame
import os

def select_image(image_folder="images", window_size=(800, 600)):
    """
    Интерфейс для выбора картинки из указанной папки.

    :param image_folder: Путь к папке с изображениями.
    :param window_size: Размер окна в пикселях (ширина, высота).
    :return: Путь к выбранной картинке или None, если выбор отменён.
    """
    # Инициализация Pygame
    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = window_size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Выбор картинки")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    # Список изображений
    try:
        images = [os.path.join(image_folder, img) for img in os.listdir(image_folder)
                  if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        print(f"Папка {image_folder} не найдена!")
        return None

    if not images:
        print(f"В папке {image_folder} нет подходящих изображений!")
        return None

    # Шрифт
    font = pygame.font.Font(None, 36)

    # Функция отображения текста
    def render_text(text, x, y, center=True):
        text_surface = font.render(text, True, BLACK)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2
        screen.blit(text_surface, (x, y))

    # Основной цикл
    running = True
    selected_image = None
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
                mouse_x, mouse_y = event.pos
                for i, img_path in enumerate(images):
                    rect = pygame.Rect(50, 50 + i * 110, 700, 100)
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_image = img_path
                        running = False

        # Отображение списка изображений
        for i, img_path in enumerate(images):
            rect = pygame.Rect(50, 50 + i * 110, 700, 100)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            render_text(os.path.basename(img_path), rect.centerx, rect.centery)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return selected_image
