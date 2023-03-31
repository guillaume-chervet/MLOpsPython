import logging
import unittest
from pathlib import Path

from model.model import Model
from model.pdf import Pdf

BASE_PATH = Path(__file__).resolve().parent


class TestModel(unittest.TestCase):
    # Set log level to info
    logging.getLogger().setLevel(logging.INFO)
    mail_extract_model = Model(logging, None, Pdf())

    def test_preprocess_scanned_pdf(self):
        # Arrange
        mail_path = BASE_PATH / 'input/filesample_scanned_pdf.pdf'

        # Act
        with open(mail_path, 'rb') as file:
            converted = self.mail_extract_model.execute(file, file.name)
            print(converted)
            # Assert
            self.assertFalse(converted["content_extracted"])
            self.assertEqual(0, len(converted["content"]))
            self.assertEqual(0, len(converted["pages_as_bytes"]))

    def test_preprocess_text_pdf(self):
        # Arrange
        mail_path = BASE_PATH / 'input/filesample_pdf.pdf'

        # Act
        with open(mail_path, 'rb') as file:
            converted = self.mail_extract_model.execute(file, file.name)
            # Assert
            self.assertTrue(converted["content_extracted"])
            self.assertEqual(919, len(converted["content"]))
            self.assertEqual(0, len(converted["pages_as_bytes"]))
