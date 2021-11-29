import re
import os
from collections import defaultdict
import nbformat
from nbconvert import LatexExporter
from pathlib import Path


class cell_extractor:
    def __init__(self,book_name:str) -> None:
        self.__valid_book_name(book_name)
        self.book_name = Path(book_name)
        self.data_folder = Path("cell_data")
        self.TEMPLATE_TPLX = Path(os.environ.get("TEMPLATE_TPLX"))
        self.TREEGUIDE = Path(os.environ.get("TREEGUIDE"))
        self.CUSTOM_TEMPLATE = self.data_folder /"templates"/"index.tex.j2"
        self.OUTPUT_FILES_DIR = self.data_folder / "images"
        self.CUSTOM_TEMPLATE_DIR = self.data_folder / "templates"
        self.MAIN_TEX = self.data_folder / "main_tex"
        self.OUTPUT_CELLS_TEX = self.data_folder / "cells"
        self.OUTPUT_FILTER_CELLS_TEX = self.data_folder/ "filtered_cells"
        
        self.__create_dir_tree()
        self.__create_readme()
    
    def export_cells(self,filter_cell:bool = True)->None:
        """
        Exports the Jupyter Lab Cells to latex code
        """
        book_path = self.book_name.resolve()
        note = nbformat.read(book_path, as_version=4)
        group = self.group_cells(note)
        latex_exporter = LatexExporter()
        self.__export_format()
        self.__create_main()
        
        latex_exporter.template_file = str(self.CUSTOM_TEMPLATE) # needs a unicode string -_-

        for (tag, g) in group.items():
            book = nbformat.v4.new_notebook()
            book.cells.extend(g)
            # unique_key will be prefix of image
            (body, resources) = latex_exporter.from_notebook_node(
                book,
                resources={
                    'output_files_dir': self.OUTPUT_FILES_DIR,
                    'unique_key': tag,
                    
                }
                )
            ofile = self.OUTPUT_CELLS_TEX / (str(tag) + ".tex") # ofile = os.path.join(OUTPUT_CELLS_TEX, ofile) # save to common folder
            
            with open(ofile, 'w') as fout:
                fout.write(body)
                print("created:", ofile)
        
            for filename, data in resources.get('outputs', {}).items():
                with open(filename, 'wb') as fres:
                    fres.write(data)
                    print("created:", filename)
        if filter_cell:
            self.__filter_cells()
    

    def __create_readme(self):
        """
        Creates a readme document to explain how to export the files to your Latex documebt
        """
        README_path = self.data_folder/ "README.md"
        if not README_path.exists():
            with open(README_path,"w") as fout:
                with open(self.TREEGUIDE,"r") as fin:
                    text = fin.read()
                    fout.write(text)

    @staticmethod
    def __valid_book_name(name)->None:
        # checks for valid book path
        if name[-6:] != ".ipynb":
            raise ValueError("Not supported file")

    
    def __create_dir_tree(self)->None:
        if not self.data_folder.exists():
            # create the directory tree
            self.data_folder.mkdir()
            self.MAIN_TEX.mkdir()
            self.OUTPUT_FILES_DIR.mkdir()
            self.CUSTOM_TEMPLATE_DIR.mkdir()
            self.OUTPUT_CELLS_TEX.mkdir()
            self.OUTPUT_FILTER_CELLS_TEX.mkdir()
    
    
    def __filter_cells(self):
        #print("Starting to filter cells")
        for tex_file in self.OUTPUT_CELLS_TEX.glob("*.tex"):
            
            with open(tex_file,"r") as texfile:
                filetext = texfile.read()
            
            
            first_line_pattern = re.compile(r"^    \\maketitle",re.M)
            last_line_pattern = re.compile(r"^\\end{document}$",re.M)

            search_first_line = first_line_pattern.search(filetext)
            search_last_line = last_line_pattern.search(filetext)

            pos_first_line = search_first_line.start()
            pos_last_line = search_last_line.start() # returns the cell ouput
            #cell_output = filetext[pos_first_line+17: pos_last_line]
            cell_output = filetext[pos_first_line+2: pos_last_line]
            format_ouput = filetext[:pos_first_line] 
            format_ouput = format_ouput.replace(r"\documentclass[11pt]{article}","")
            format_ouput = format_ouput.replace(r"\title{Notebook}","")
            
            filter_cell_path = self.OUTPUT_FILTER_CELLS_TEX / tex_file.name
            with open(filter_cell_path,"w") as filter_cell_tex:
                filter_cell_tex.write(cell_output)
            filter_format_path = self.OUTPUT_FILTER_CELLS_TEX / "format.tex"
            with open(filter_format_path,"w") as format_tex:
                format_tex.write(format_ouput)

    
    @staticmethod
    def group_cells(note):
        # if sames tags are found group it to same list
        pattern = re.compile(r'^#latex:(.*?)$(\n?)', re.M) #`^#latex:(.*)`
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

    
    
        
    def __export_format(self):
        """
        Exports the format to add to the .sty file that should be added to the main.tex file
        """
        
        template = self.TEMPLATE_TPLX 
        target_template = self.CUSTOM_TEMPLATE
        with open(target_template, 'w') as ftarget:
            with open(template) as fsrc:
                for line in fsrc:
                    # replace the line so than it does not contain macro definition
                    if line == "((*- extends 'base.tplx' -*))\n":
                        line = "((*- extends 'document_contents.tplx' -*))\n"
                    ftarget.write(line)
        

    def __create_main(self):
        # creates `main.tex` which only has macro definition
        latex_exporter = LatexExporter()
        book = nbformat.v4.new_notebook()
        book.cells.append(
            nbformat.v4.new_raw_cell(r'\input{__your_input__here.tex}'))
        (body, _) = latex_exporter.from_notebook_node(book)
        with open(self.MAIN_TEX/"main.tex", 'w') as fout:
            fout.write(body)
       