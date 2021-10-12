## Jupyter Notebook Cell Extractor
This a little library to extract Jupyter Notebook (.ipynb) cells.  

## Usage
The basics of this programm are described [here](https://stackoverflow.com/questions/55057888/difficult-workflow-writing-latex-book-full-of-python-code) by its original author. This is an adaptation due to deprecation or change in versions.  

The cell extraction works by adding the tag ```#latex:tag_0``` to the cell.  Cells with the same tag will be exported to the same directory. In case there is no tag, the cell wont be exported.  

![cell](assets/img/cell_tag.png)  

Once the programm is executed, a couple of directorys will be created inside the parent dir. The important one is: ```filtered_cells```. It will create also a ```format.tex``` file which needs to be copyed inside your ```main.tex```. The filtered cells can be copyed and pasted to wherever you need them to be added. The next image shows a little example of the exported cells:
![exported_cell](assets/img/exported_cell_example.png)
### Using it as a script(will not continue to be developed)
You need to download the [main.py](https://github.com/jaimebw/jupyter_cell_extractor/blob/main/src/jupyter_cell_extractor/main.py) file plus the data folder, and run the ```main.py``` file as explained [here](https://stackoverflow.com/questions/55057888/difficult-workflow-writing-latex-book-full-of-python-code) and in the next lines:
```
python main.py init
python main.py book_name.ipynb
```  
In case you want to use your own .tplx file, you need to delete the one inside the ```data``` dir and put yours inside it. 
### Using it as library (may suffer changes in the future)
You need to install it:
```
pip install jupyter-cell-extractor
```
The second way that it is still in development but it is intended to work by executing the code directly from the Jupyter Lab interface. You need to previusly add the ```#latex:tag_0``` to the cells you are interested in exporting. 
```python
from jupyter_cell_extractor.main import *
get_cells(book_name)
```
## Styling the cells  
You can use a different style for the cells by changing the ```.tplx``` template. In this library I'm using this [one](https://github.com/t-makaro/nb_pdf_template/blob/master/nb_pdf_template/templates/classic.tplx)
## To do-list 

* Create tests
* Better the code

Contributions are welcomed!! 

