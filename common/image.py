from pathlib import Path

#create image path

class Image:
    __images_path = None

    @staticmethod
    def get_images_path():
        home_path = Path(__file__).parent.parent
        images_path = home_path.joinpath('static/media')

        if not images_path.exists():
            images_path.mkdir(parents=True)

        return images_path