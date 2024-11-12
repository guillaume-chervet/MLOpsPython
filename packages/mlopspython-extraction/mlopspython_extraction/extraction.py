import io
from abc import abstractmethod, ABC
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, List

import fitz
from fitz import Pixmap

import imageio


def convert_pixmap_to_rgb(pixmap) -> Pixmap:
    """Convert to rgb in order to write on png"""
    # check if it is already on rgb
    if pixmap.n < 4:
        return pixmap
    else:
        return fitz.Pixmap(fitz.csRGB, pixmap)


@dataclass
class ImageResult:
    image_bytes_io: BytesIO
    index_page: int
    index_image: int


def extract_images_stream(trailer_path) -> Iterable[ImageResult]:
    reader = imageio.get_reader(trailer_path)
    total_frames = reader.count_frames()
    interval = max(total_frames // 50, 1)
    
    for i in range(total_frames):
        if i % interval == 0:
            image = reader.get_data(i)
            image_bytes_io = BytesIO()
            imageio.imwrite(image_bytes_io, image, format="jpg")
            image_bytes_io.seek(0)

            yield ImageResult(image_bytes_io, 0, i)


@dataclass
class ExtractImagesResult:
    number_files_input: int
    number_images_output: int


class IDataManager(ABC):
    @abstractmethod
    def get_movie_trailers(self, trailers_directory_path: str) -> List[Path]:
        pass

    @abstractmethod
    def save_image(self, image_stream: ImageResult, images_directory_path: str) -> None:
        pass

    @abstractmethod
    def create_directory(self, directory_path: str) -> None:
        pass


class DataManager(IDataManager):
    def get_movie_trailers(self, trailers_directory_path: str) -> List[Path]:
        trailers = [mt for mt in Path(trailers_directory_path).iterdir() if mt.is_file() and mt.suffix == ".mp4"]
        trailers.sort()
        return trailers

    def save_image(self, image_bytes_io: io.BytesIO, image_path: str) -> None:
        with open(image_path, "wb") as file_stream:
            file_stream.write(image_bytes_io.getbuffer())

    def create_directory(self, directory_path: str) -> None:
        Path(directory_path).mkdir(parents=True, exist_ok=True)


class ExtractImages:
    def __init__(self, data_manager: IDataManager):
        self.data_manager = data_manager

    def extract_images(self, trailers_directory_path: str, images_directory_path: str) -> ExtractImagesResult:
        manager = self.data_manager
        trailers = manager.get_movie_trailers(trailers_directory_path)
        print("[DEBUG] Found {0} trailers".format(len(trailers)))
        manager.create_directory(images_directory_path)
        number_images_output = 0
        for trailer_path in trailers:
            for image_stream in extract_images_stream(trailer_path):
                filename = "{0}_image{1}.png".format(trailer_path.stem, str(image_stream.index_image))
                print("[DEBUG] Saving image {0}".format(filename))
                number_images_output = number_images_output + 1
                manager.save_image(image_stream.image_bytes_io, str(Path(images_directory_path) / filename))

        return ExtractImagesResult(number_files_input=len(trailers), number_images_output=number_images_output)
