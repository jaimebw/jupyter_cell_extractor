import sys
import re
import os
from collections import defaultdict
import nbformat
from nbconvert import LatexExporter
import glob
import shutil

OUTPUT_FILES_DIR = './images'
CUSTOM_TEMPLATE = './templates/index.tex.j2' 
CUSTOM_TEMPLATE_DIR = './templates'
MAIN_TEX = 'main.tex'
OUTPUT_CELLS_TEX = "./cells"
OUTPUT_FILTER_CELLS_TEX = "./filtered_cells"
TEMPLATE_TPLX = os.environ.get("TEMPLATE_TPLX")
def create_main():
    
    # creates `main.tex` which only has macro definition
    latex_exporter = LatexExporter()
    book = nbformat.v4.new_notebook()
    book.cells.append(
        nbformat.v4.new_raw_cell(r'\input{__your_input__here.tex}'))
    (body, _) = latex_exporter.from_notebook_node(book)
    with open(MAIN_TEX, 'x') as fout:
        fout.write(body)
    print("created:", MAIN_TEX)


def init():
    create_main()
    latex_exporter = LatexExporter()
    # copy `style_ipython.tplx` in `nbconvert.exporters` module to current directory,
    # and modify it so that it does not contain macro definition
    """
    tmpl_path = os.path.join(
        os.path.dirname(exporters.__file__),
        latex_exporter.template_paths[9]) # Aquí es donde he guardo la template que me ha gustado
    src = os.path.join(tmpl_path, 'classic.tplx') # Nombre de la template
    """
    src = TEMPLATE_TPLX
    src = os.path.abspath(src)
    print(src)
    target = CUSTOM_TEMPLATE
    
    with open(src) as fsrc:
        if not os.path.exists(CUSTOM_TEMPLATE_DIR):
            os.mkdir(CUSTOM_TEMPLATE_DIR)
        with open(target, 'w') as ftarget:
            for line in fsrc:
                # replace the line so than it does not contain macro definition
                if line == "((*- extends 'base.tplx' -*))\n":
                    line = "((*- extends 'document_contents.tplx' -*))\n"
                ftarget.write(line)
    print("created:", CUSTOM_TEMPLATE)


def group_cells(note):
    # scan the cell source for tag with regexp `^#latex:(.*)`
    # if sames tags are found group it to same list
    pattern = re.compile(r'^#latex:(.*?)$(\n?)', re.M)
    group = defaultdict(list)
    for num, cell in enumerate(note.cells):
        m = pattern.search(cell.source)
        if m:
            tag = m.group(1).strip()
            # remove the line which contains tag
            cell.source = cell.source[:m.start(0)] + cell.source[m.end(0):]
            group[tag].append(cell)
        else:
            print("tag not found in cell number {}. ignore".format(num + 1))
    return group


def doit(book_name = None):
    
    if book_name == None:
        with open(sys.argv[1]) as f:
            note = nbformat.read(f, as_version=4)
    else:
        with open(book_name) as f:
            note = nbformat.read(f, as_version=4)
    
    group = group_cells(note)
    latex_exporter = LatexExporter()
    
    latex_exporter.template_file = CUSTOM_TEMPLATE
    
    try:
        os.mkdir(OUTPUT_FILES_DIR)
    except FileExistsError:
        pass
    try:
        os.mkdir(OUTPUT_CELLS_TEX)
    except FileExistsError:
        pass
    for (tag, g) in group.items():
        book = nbformat.v4.new_notebook()
        book.cells.extend(g)
        # unique_key will be prefix of image
        (body, resources) = latex_exporter.from_notebook_node(
            book,
            resources={
                'output_files_dir': OUTPUT_FILES_DIR,
                'unique_key': tag,
                
            }
            )
        ofile = tag + '.tex'
        ofile = os.path.join(OUTPUT_CELLS_TEX, ofile) # save to common folder
        with open(ofile, 'w') as fout:
            fout.write(body)
            print("created:", ofile)
     

        for filename, data in resources.get('outputs', {}).items():
            with open(filename, 'wb') as fres:
                fres.write(data)
                print("created:", filename)


def get_cells(book_name,clean_folders= True):
    if not os.path.exists("main.tex"):
        init()
    try:
        doit(book_name)
        filter_cells()
        if clean_folders == True:
            for i in [CUSTOM_TEMPLATE_DIR,OUTPUT_CELLS_TEX]:
                shutil.rmtree(i)
            os.remove("main.tex")
    except:
        print("Book not found")


def filter_cells():
    print("Starting to filter cells")
    for tex_file in glob.glob(OUTPUT_CELLS_TEX+"/**/*.tex",recursive=True):
        _,TEX_FILE_NAME = os.path.split(tex_file) 
        texfile = open(tex_file,'r')
               
        filetext = texfile.read()
        texfile.close()
        first_line_pattern = re.compile(r"^\\begin{document}$",re.M)
        last_line_pattern = re.compile(r"^\\end{document}$",re.M)

        search_first_line = first_line_pattern.search(filetext)
        search_last_line = last_line_pattern.search(filetext)

        pos_first_line = search_first_line.start()
        pos_last_line = search_last_line.start() # returns the cell ouput
        cell_output = filetext[pos_first_line+17: pos_last_line]
        format_ouput = filetext[:pos_first_line] 
        format_ouput = format_ouput.replace(r"\documentclass[11pt]{article}","")
        format_ouput = format_ouput.replace(r"\title{Notebook}","")
        
        if not os.path.exists(OUTPUT_FILTER_CELLS_TEX):
            os.mkdir(OUTPUT_FILTER_CELLS_TEX)
        
        cell_text = open(os.path.join(OUTPUT_FILTER_CELLS_TEX,TEX_FILE_NAME),"w")
        format_text = open("format.tex","w")

        
        
        cell_text.write(cell_output)
        format_text.write(format_ouput)

        cell_text.close()
        format_text.close()


if __name__ == '__main__':
    this_dir, _= os.path.split(__file__)
    TEMPLATE_TPLX = glob.glob("{}/data/**/*.tplx".format(this_dir),recursive=True)[0]
    if len(sys.argv) <= 1:
        print("USAGE: this_script [init|yourfile.ipynb]")
    elif sys.argv[1] == "init":
        init()
    else:

        doit()
        filter_cells()