from src.jupyter_cell_extractor import cell_extractor

def test_lib():
    #print("Testing lib implementation")
    cell = cell_extractor("/Users/jaime/repos/jupyter_cell_extractor/tests/test_book.ipynb") 
    cell.export_cells()
    



