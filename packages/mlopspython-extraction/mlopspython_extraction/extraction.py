import io
from abc import abstractmethod, ABC
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, List

import fitz
from fitz import Pixmap


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


def extract_images_stream(pdf_bytes) -> Iterable[ImageResult]:
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        number_pages = len(document) - 1
        for index_page in range(number_pages):
            images = document.get_page_images(index_page)
            for index_image, image in enumerate(images):
                xref = image[0]
                image_pix = fitz.Pixmap(document, xref)
                image_bytes_io = BytesIO(convert_pixmap_to_rgb(image_pix).tobytes())
                yield ImageResult(image_bytes_io, index_page, index_image)


@dataclass
class ExtractImagesResult:
    number_files_input: int
    number_images_output: int


class IDataManager(ABC):
    @abstractmethod
    def get_pdf_files(self, pdfs_directory_path: str) -> List[Path]:
        pass

    @abstractmethod
    def save_image(self, image_stream: ImageResult, images_directory_path: str) -> None:
        pass

    @abstractmethod
    def create_directory(self, directory_path: str) -> None:
        pass


class DataManager(IDataManager):
    def get_pdf_files(self, pdfs_directory_path: str) -> List[Path]:
        pdfs = [p for p in Path(pdfs_directory_path).iterdir() if p.is_file() and p.suffix == ".pdf"]
        pdfs.sort()
        return pdfs

    def save_image(self, image_bytes_io: io.BytesIO, image_path: str) -> None:
        with open(image_path, "wb") as file_stream:
            file_stream.write(image_bytes_io.getbuffer())

    def create_directory(self, directory_path: str) -> None:
        Path(directory_path).mkdir(parents=True, exist_ok=True)


class ExtractImages:
    def __init__(self, data_manager: IDataManager):
        self.data_manager = data_manager

    def extract_images(self, pdfs_directory_path: str, images_directory_path: str) -> ExtractImagesResult:
        manager = self.data_manager
        pdfs = manager.get_pdf_files(pdfs_directory_path)
        manager.create_directory(images_directory_path)
        number_images_output = 0
        for pdf_path in pdfs:
            with open(pdf_path, "rb") as pdf_stream:
                pdf_bytes = pdf_stream.read()
            for image_stream in extract_images_stream(pdf_bytes):
                filename = "{0}_page{1}_index{2}.png".format(pdf_path.stem, str(image_stream.index_page),
                                                             str(image_stream.index_image))
                number_images_output = number_images_output + 1
                manager.save_image(image_stream.image_bytes_io, str(Path(images_directory_path) / filename))

        return ExtractImagesResult(number_files_input=len(pdfs), number_images_output=number_images_output)
