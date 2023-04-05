import logging
import unittest
from pathlib import Path

from ..core.base_app_settings import BaseAppSettings
from ..core.model.model import Model


class TestProcess(unittest.IsolatedAsyncioTestCase):

    def test_process(self):
        model = Model(logging, BaseAppSettings(logging))
        dir = "./tests/gt/f2b68110-3b7b-4cc1-98fc-caf451d71ff2/mlcli"
        dest = "./tests/diff"
        flist = [p for p in Path(dir).iterdir() if p.is_file()]
        for fp in flist:
            with open(fp, "rb") as pdf_stream:
               cvr = model.execute(pdf_stream, fp.name, {"type": "opencv"})
            with open(fp, "rb") as pdf_stream:
                pr = model.execute(pdf_stream, fp.name, {"type": "pillow"})
            if(cvr[0]["prediction"] != pr[0]["prediction"]):
                print(fp.name)
                destination_path = Path(dest) / fp.name
                destination_path.write_bytes(fp.read_bytes())

