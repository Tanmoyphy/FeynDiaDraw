# QGRAF Diagram Drawer (Requirements: Python2, LuaLatex)
## Dependencies
This code uses [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) and [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman)

## Use

The program *FeynDiaDraw* is a Python program for drawing Feynman diagrams. The code translates [QGRAF](http://cfif.ist.utl.pt/~paulo/qgraf.html) diagrams  into a *LuaLaTeX* file using [tikz-feynman](https://github.com/JP-Ellis/tikz-feynman) to draw them after compilation

### QGRAF
The program is provided with a *QGRAF* style file called `xmldraw.sty`. Any set of Feynman rules compatible with *QGRAF* can be handled, and the output should be put in the package folder to be processed.

## Run
*fdraw.pyc* is an encoded python2 file. All the information about particles has been given there. To run it, make sure to have the QGRAF generated output file, then use

```
python2 fdraw.pyc
```

This should be compiled, and the QGRAF file should be asked for. It should return the following interface:
```
Welcome to FeynDiaDraw!
----------------------------------FeynDiaDraw-----------------------------------
Version: 1.0.1
Copyright 2024, tanmoy.pati@niser.ac.in
--------------------------------------------------------------------------------
Enter the QGRAF output file in xmld format: 
```

Give the file name with the extension. The *diagrams.tex* file will be generated with appropriately formatted LaTex code.

Next, go to the TeX folder. Change the input file name of the *main.tex* file. For instance 

```
\include{diagrams}
```

Now, run using *LuaLaTeX* with

```
lualatex main.tex
```

There might be some overflow errors, but do not care, these are not fatal error. A pdf will be generated with diagram numbers.

## Limitations

The code is designed to make loop diagrams look nice. At the moment, it returns a `ValueError` if two vertices are joined by 4 or more propagators.

## Citing

Help is taken from (https://github.com/ndeutschmann/qgraf-xml-drawer). The original code is citeable using the following DOI:

[![DOI](https://zenodo.org/badge/59492920.svg?maxAge=0)](https://zenodo.org/badge/latestdoi/59492920)
