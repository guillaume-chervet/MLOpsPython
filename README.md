# MLOpsPython

Set up Python python 3.10.9 on your laptop. You can use venv, conda, etc.

Download PyCharm Pro: https://www.jetbrains.com/pycharm/

First, create git name "MLOpsPython" on your own github account.

```bash
git clone https://github.com/yourusername/MLOpsPython
cd MLOpsPython
# Exclude Pycharm local files from git
echo ".idea" > .gitignore 
```

```bash
git clone https://github.com/yourusername/MLOpsPython
cd MLOpsPython
mkdir train
cd train
```

Initialize extraction step.
```bash
mkdir extraction
cd extraction
git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others
echo "dataset-cats-dogs-others
extracted_images" > .gitignore 
```

Create requirements.txt
```bash
echo "pymupdf===1.21.1" > requirements.txt
pip install ()r requirements.txt
```

Create extraction.py
```bash
echo 'from io import BytesIO
from pathlib import Path
import fitz
from fitz import Document, Pixmap

def convert_pixmap_to_rgb(pixmap) -> Pixmap:
    """Convert to rgb in order to write on png"""
    # check if it is already on rgb
    if pixmap.n < 4:
        return pixmap
    else:
        return fitz.Pixmap(fitz.csRGB, pixmap)

pdfs_directory_path = ".\dataset-cats-dogs-others"
images_directory_path = ".\extracted_images"

Path(images_directory_path).mkdir(parents=True, exist_ok=True)
files = [p for p in Path(pdfs_directory_path).iterdir() if p.is_file()]
for path in files:
    with open(path, "rb") as str:
        with fitz.open(stream=str.read(), filetype="pdf") as d:
            file_images = []
            nb = len(d) - 1
            for i in range(nb):
                page = d[i]
                imgs = d.get_page_images(i)
                nb_imgs = len(imgs)
                for j, img in enumerate(imgs):
                    xref = img[0]
                    pix = fitz.Pixmap(d, xref)
                    bytes = BytesIO(convert_pixmap_to_rgb(pix).tobytes())
                    fn = path.stem + "_page" + str(i) + "_index" + str(j) + ".png"
                    with open(images_directory_path + "\\" + fn, "wb") as f:
                        f.write(bytes.getbuffer())' > extraction.py
```

Clean code using PyCharm shorcut.

Create a tests directory and create a extraction_test.py file.

```bash
mkdir tests
cd tests
```

extraction_test.py
```bash
echo "import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        value = 'foo'.upper()
        expected = 'FOO'
        self.assertEqual(value, expected)

if __name__ == '__main__':
    unittest.main()" > extraction_test.py
```

You can run unit test manually
```bash
python -m unittest tests.extraction_test
```

You can now code and debug a real unit test for extraction.py from PyCharm your first unit test.

Coverage
```bash
pip install coverage
coverage run -m unittest tests.extraction_test  #--omit tests
coverage report
coverage html
```

Now you can commit then push your code on github.

We are going to create a github action to run unit tests on each commit.

