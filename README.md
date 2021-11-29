## Jupyter Notebook Cell Extractor
This a little library to extract Jupyter Notebook (.ipynb) cells.  

## Usage
The basics of this programm are described [here](https://stackoverflow.com/questions/55057888/difficult-workflow-writing-latex-book-full-of-python-code) by its original author. This is an adaptation due to deprecation or change in versions.  

The cell extraction works by adding the tag ```#latex:tag_0``` to the cell.  Cells with the same tag will be exported to the same directory. In case there is no tag, the cell wont be exported.  

![cell](assets/img/cell_tag.png)  

Once the programm is executed, a couple of directorys will be created inside the parent dir. The important one is: ```filtered_cells``` and ```images```. It will create also a ```format.tex``` file which needs to be copyed inside your ```main.tex```. The filtered cells can be copyed and pasted to wherever you need them to be added. The next image shows a little example of the exported cells:
![exported_cell](assets/img/exported_cell_example.png)

### Using it as library 
You need to install it:
```
pip install jupyter-cell-extractor
```  
And run the next command in a cell or script:
```python
from jupyter_cell_extractor import cell_extractor
cell = cell_extractor("your_book_name.ipynb") 
cell.export_cells()
```
## Styling the cells  
In case you want to use your own .tplx file, the option will be added in the future
You can use a different style for the cells by changing the ```.tplx``` template. In this library I'm using this [one](https://github.com/t-makaro/nb_pdf_template/blob/master/nb_pdf_template/templates/classic.tplx)
## To do-list 

* Better the code
* Add more functionalities

Contributions are welcomed!! 

