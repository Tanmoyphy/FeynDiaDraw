from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from copy import copy
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dep'))
from vertex import *
from propagator import *

if __name__ == "__main__":
    print("FeynDiaDraw".center(80, "-"))
    print("Version: 1.0.5")
    print("Copyright 2025, tanmoy.pati@niser.ac.in")
    print("-" * 80)
    
    print("\033[1mWelcome to FeynDiaDraw!\033[0m")
    
    print("Python Version Check:")
    if sys.version_info[0] < 3:
       print("\033[1mError: This script requires minimum Python 3. Please run it with 'python3 your_script_name.py'\033[0m\n")
       sys.exit(1)
    else:
       print("\033[1mPython 3 version is up-to-date for this software.\033[0m\n")

    INPUT = input("Enter the QGRAF output file in xmld format: ")
    print("")
    print("Noted! Processing the file...")

    graphs = XML(default_loader(INPUT, parse))
    diagrams = graphs.find("diagrams")

    print("")
    print("Diagrams extracted successfully!")
    print("")
    print("Note: Lualatex arranges the diagrams automatically, hence there is a possibility\n of having too many or too few diagrams in a page")
    print("Please enter the number of diagrams you need in a single row:")
    numr = int(input(">>> "))

    pt = {}
    with open('dep/particles.txt', 'r') as text_file:
        for line in text_file:
            key, value = line.strip().split(': ')
            pt[key] = value
    with open("TeXpreamble1.tex", "w") as file1:
        file1.write("\\documentclass{article}\n")
        file1.write("\\usepackage{subcaption}\n")
        file1.write("\\usepackage{graphicx}\n")
        file1.write("\\usepackage{multicol}\n")
        file1.write("\\usepackage[squaren,Gray]{SIunits}\n")
        file1.write("\\usepackage{multirow}\n")
        file1.write("\\usepackage{makecell}\n")
        file1.write("\\usepackage[compat=1.1.0]{tikz-feynman}\n")
        file1.write("\\usepackage[textsize=tiny,backgroundcolor=white]{todonotes}\n")
        file1.write("\\usepackage[top=1in, bottom=1.25in, left=0.8in, right=0.8in]{geometry}\n")
        file1.write("\\begin{document}\n")
    with open("TeXpreamble2.tex", "w") as file2:
        file2.write("\\end{document}\n")
    with open("diagrams.tex", "w") as file:
        diagram_count = len(list(diagrams))
        current_diagram = 0

        for diagram in diagrams: 
            DiagID = diagram.find("id").text
            current_diagram += 1
            sys.stdout.write("\rProcessing diagrams: %d/%d" % (current_diagram, diagram_count))
            sys.stdout.flush()
            file.write("\\begin{subfigure}{0.2\\textwidth}\n")
            file.write("\\feynmandiagram[small]{" + "%diagram_number_" + DiagID + "\n")

            propagators = []
            for p in diagram.find("propagators"):  
                propagators.append(propagator(p))

            vertices = []
            for v in diagram.find("vertices"): 
                vertices.append(Vertex(v))

            bundles = []
            for p in propagators:
                if bundles: 
                    found = False
                    for b in bundles:
                        if p.fromto == b[0].fromto:
                            b.append(p)
                            found = True
                            break
                    if not found:
                        bundles.append([p])
                else:
                    bundles = [[p]]

            for b in bundles:
                if len(b) == 1:
                    if b[0].vfrom != b[0].vto:
                        b[0].texprint(file, pt)
                    else:  
                        tadfrom = copy(b[0])
                        tadto = copy(b[0])
                        tadfrom.vto = "tad" + tadfrom.id
                        tadto.vfrom = "tad" + tadfrom.id
                        shape = "half right"
                        tadfrom.texprint(file, pt, shape)
                        tadto.texprint(file, pt, shape)
                elif len(b) == 2: 
                    shapedict = ["quarter right", "quarter left"]
                    b[0].texprint(file, pt, shapedict[0])
                    b[1].texprint(file, pt, shapedict[1] if b[1].vfrom == b[0].vfrom else shapedict[0])  # Combined condition
                elif len(b) == 3:  
                    shapedict = ["quarter right", "quarter left"]
                    b[0].texprint(file, pt, shapedict[0])
                    b[1].texprint(file, pt, shapedict[1] if b[1].vfrom == b[0].vfrom else shapedict[0])  # Combined
                    b[2].texprint(file, pt)
                elif len(b) > 4: 
                    print("I don't know how to deal with this !")
                    raise ValueError('Too many propagators in a bundle')

            for v in vertices:
                for i in range(len(v.fields)):
                    if re.search(r'[a-zA-Z]', v.fields[i]):
                        file.write("{} [particle=] -- [{}] {},\n".format(v.fields[i], pt[v.types[i]], v.id))

            file.write("};\n")
            file.write("\\caption*{"+INPUT.replace(".x", "$\\_$") + DiagID + "}\n")
            file.write("\\end{subfigure}\n")


    with open('diagrams.tex', 'r') as f:
        content = f.read()

    subfigures = re.findall(r'\\begin{subfigure}.*?\\end{subfigure}', content, re.DOTALL)

    output = '\\begin{figure}\n\\centering\n'

    counter = 0

    for subfigure in subfigures:
        output += subfigure + '\n'
        counter += 1
        if counter % numr == 0 and counter != len(subfigures):
            output += '\\end{figure}\n'
            output += '\n\\begin{figure}\n\\centering\n'

    output += '\n\\end{figure}\n'

    with open('diagrams.tex', 'w') as f:
        f.write(output)

    with open('diagrams.tex', 'r') as f:
        content = f.read()

    subfigures = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)

    output = '\n'

    counter = 0

    for subfigure in subfigures:
        output += subfigure + '\n'
        counter += 1
        if counter % 8 == 0 and counter != len(subfigures):
            output += '\\clearpage\n'

    with open('diagrams.tex', 'w') as f:
        f.write(output)

    print("\n")
    print("Done! No error encountered\n")
    
def merge_three_files(destination_file, source_file1, source_file2, source_file3):
    """Merges the contents of three files at the end of a destination file (Python 3)."""

    try:
        with open(destination_file, "w") as dest_file:
            with open(source_file1, "r") as src_file1:
                dest_file.write(src_file1.read())
            with open(source_file2, "r") as src_file2:
                dest_file.write(src_file2.read())
            with open(source_file3, "r") as src_file3:
                dest_file.write(src_file3.read())
        print(f"The generated file is ",INPUT.replace(".x", ".tex"),"\n")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
merge_three_files("QGRAF2TeX.tex", "TeXpreamble1.tex", "diagrams.tex", "TeXpreamble2.tex")
try:
    os.rename("QGRAF2TeX.tex", INPUT.replace(".x", ".tex"))
except FileNotFoundError:
    print("Error: QGRAF2TeX.tex not found.")
except FileExistsError:
    print(f"Error: A file named {INPUT.replace('.x', '.tex')} already exists.")
except PermissionError:
    print("Error: Permission denied.")
except OSError as e:
    print(f"Error: An OS error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
os.remove("TeXpreamble1.tex")
os.remove("TeXpreamble2.tex")
os.remove("diagrams.tex")
