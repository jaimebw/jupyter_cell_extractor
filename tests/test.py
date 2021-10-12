from src.jupyter_cell_extractor.main import *
from subprocess import call


def test_lib():
    print("Testing lib implementation")
    get_cells("test_book.ipynb")


def test_script():
    print("Testing scripts implementation")
    call(" python ../src/jupyter_cell_extractor/main.py init",shell= True)
    call(" python ../src/jupyter_cell_extractor/main.py test_book.ipynb",shell =True)
    



