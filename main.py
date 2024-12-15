from ascii import ArtASCIIGray, ArtASCIIColor
from pixel import ArtPixelGray, ArtPixelColor
from interface import PickPicture, PickArt


if __name__ == '__main__':

    while True:
        picture = PickPicture("photo")
        selected_path = picture.select_event()
        art = PickArt()
        select_art = art.select_event()

        if selected_path:
            print(f"Вы выбрали: {selected_path}")
        else:
            print("Выбор отменён или изображение не выбрано.")\

        match select_art:
            case 'ASCII':
                app = ArtASCIIGray(selected_path)
                app.run()
            case 'ASCII Color':
                app = ArtASCIIColor(selected_path)
                app.run()
            case 'PIXEL':
                app = ArtPixelGray(selected_path)
                app.run()
            case 'PIXEL Color':
                app = ArtPixelColor(selected_path)
                app.run()

