from ascii import ArtASCIIColor
from pixel import ArtPixel
from interface import select_image


if __name__ == '__main__':

    selected_path = select_image(image_folder="photo")

    if selected_path:
        print(f"Вы выбрали: {selected_path}")
    else:
        print("Выбор отменён или изображение не выбрано.")

    app = ArtPixel(selected_path)
    app.run()