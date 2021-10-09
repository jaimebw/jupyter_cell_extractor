from setuptools import find_packages, setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
        name = 'jupyter_cell_extractor',
        version='0.1.0'
        description= "Jupyter Cell Extractor",
        long_description= long_description
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.8"
        )
