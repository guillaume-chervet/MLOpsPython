# Ajoute le dossier parent (train/label_split_data) au PYTHONPATH
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
