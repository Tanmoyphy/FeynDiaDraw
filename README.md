# QGRAF Diagram Drawer (Requirements: Python, LuaLatex)
## Dependencies
This code uses [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) and [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman)

## Use

The program *FeynDiaDraw* is a Python program for drawing Feynman diagrams. The code translates [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) diagrams  into a *LuaLaTeX* file using [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman) to draw them after compilation

### QGRAF
The program is provided with a *QGRAF* style file called `xmldraw.sty`. Any set of Feynman rules compatible with *QGRAF* can be handled, and the output should be put in the package folder to be processed.

## Run
*fdraw.py* is an python file. All the information about particles has been given there. To run it, make sure to have the QGRAF generated output file, then use

```
python3 fdraw.py
```

If Python3 is installed appropriately, this should be compiled, and the QGRAF file should be asked for (The program will automatically check for the installed version of Python3). It will return the following interface:
```
Python Version Check:
Python 3 version is up-to-date.

Welcome to FeynDiaDraw!
----------------------------------FeynDiaDraw-----------------------------------
Version: 1.0.5
Copyright 2024, tanmoy.pati@niser.ac.in
--------------------------------------------------------------------------------
Enter the QGRAF output file in xmld format: 
```

Give the file name with the extension. Next, it will ask for the number of diagrams it will keep in each row. Give an appropriate number like 2,3,... The *<qgraf_file_name>.tex* file will be generated with appropriately formatted LaTex code.


Now, run using *LuaLaTeX* with

```
lualatex <qgraf_file_name>.tex
```

There might be some overflow errors, but do not care, these are not fatal error. A pdf will be generated with diagram numbers.

### Particle info and color
 Particles in the QGRAF file can be specified and colored differently within ```FeynDiaDraw```. All this information has been stored in the ```particles.txt``` file in the ```dep``` folder. Any new particles used in QGRAF can be drawn by adding them to this file. The basic structure of particle data is:
```
<particle_name>: <particle_type>, color=<intended_color>
```
 
## Limitations

The code is designed to make loop diagrams look nice. At the moment, it returns a `ValueError` if two vertices are joined by 4 or more propagators.

## Citing

Help is taken from (https://github.com/ndeutschmann/qgraf-xml-drawer). The original code is citeable using the following DOI:

[![DOI](https://zenodo.org/badge/59492920.svg?maxAge=0)](https://zenodo.org/badge/latestdoi/59492920)
