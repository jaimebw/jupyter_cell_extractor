import os
from pathlib import Path
from .main import cell_extractor

this_dir = Path(__file__)
TEMPLATE_TPLX = this_dir.parents[0]/"data"/"classic.tplx"
TREEGUIDE = this_dir.parents[0]/"data"/"treeguide.txt"
os.environ["TEMPLATE_TPLX"] = str(TEMPLATE_TPLX)
os.environ["TREEGUIDE"] = str(TREEGUIDE)