from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from copy import copy
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dep'))
from vertex import *
from propagator import *

INPUT= "qqb2ZN3LO.xmld" #QGRAF output file
graphs=XML(default_loader(INPUT,parse))
diagrams=graphs.find("diagrams")

#Particle dictionnary. Adapt this to your model
pt = {"U": "fermion,color=red", "u": "anti fermion,color=violet", "D": "fermion,color=purple", "d": "anti fermion,color=orange", "Wp": "charged boson,color=olive","Wm": "charged boson,color=brown",
"Z": "boson,color=blue","g": "gluon,color=green","gh": "scalar,color=yellow","GH": "scalar,color=cyan", "V": "boson,color=teal", "ph": "boson,color=teal"}


file = open("diagrams.tex","w+")

for diagram in diagrams.getchildren():
    DiagID = diagram.find("id").text
    print "Creating : "+DiagID
    file.write("\\begin{subfigure}{0.2\\textwidth}""\n")
    file.write("\\feynmandiagram[small]{"+"%diagram_number_"+DiagID+"\n")
    NOpropagators=diagram.find("propagators").getchildren()
    NOvertices=diagram.find("vertices").getchildren()
    propagators=[]
    for p in NOpropagators:
        propagators.append(propagator(p))
    vertices=[]
    for v in NOvertices:
        vertices.append(Vertex(v))
    bundles = []
    for p in propagators:
        if len(bundles) > 0:
            found = False
            for b in bundles:
                if p.fromto == b[0].fromto:
                    print "adding my propagator to an existing bundle"
                    b.append(p)
                    found = True
                    break
            if not found:
                bundles.append([p])
        else:
            bundles = [[p]]
    for b in bundles:
        if len(b)==1:
            if b[0].vfrom != b[0].vto:
                b[0].texprint(file,pt)
            else: #TADPOLE
                tadfrom = copy(b[0])
                tadto = copy(b[0])
                tadfrom.vto = "tad"+tadfrom.id
                tadto.vfrom = "tad"+tadfrom.id
                shape = "half right"
                tadfrom.texprint(file,pt,shape)
                tadto.texprint(file,pt,shape)
        if len(b)==2:
            shapedict = ["quarter right", "quarter left"]

            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
        if len(b)==3:
            shapedict = ["quarter right", "quarter left"]
            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
            b[2].texprint(file,pt)
        if len(b)>4:
            print "I don't know how to deal with this !"
            raise ValueError('Too many propagators in a bundle')

    for v in vertices:
        for i in range(len(v.fields)):
            if re.search('[a-zA-Z]',v.fields[i]):
                file.write("{} [particle=] -- [{}] {},\n".format(v.fields[i],pt[v.types[i]],v.id))
#
#    file.write("ext1 -- [opacity = 0] mid,\n") add a comma above !
#    file.write("ext3 -- [opacity = 0] mid\n")
#    file.write("q -- [opacity = 0] q\n")
    file.write("};\n")
    file.write("\\caption*{dia "+DiagID+"}""\n")
    file.write("\\end{subfigure}""\n")
file.close()
    
    
# Open the LaTeX file
with open('diagrams.tex', 'r') as f:
    content = f.read()

# Find all occurrences of \begin{subfigure} and \end{subfigure}
subfigures = re.findall(r'\\begin{subfigure}.*?\\end{subfigure}', content, re.DOTALL)

# Initialize the output string
output = '\\begin{figure}\n\\centering\n'

# Initialize a counter for the number of subfigures
counter = 0

# Iterate over the subfigures
for subfigure in subfigures:
    # Add the subfigure to the output
    output += subfigure + '\n'

    # Increment the counter
    counter += 1

    # If this is the 4th, 8th, 12th,... subfigure, add a \end{figure} and a \begin{figure}
    if counter % 4 == 0 and counter!= len(subfigures):
        output += '\\end{figure}\n'
        output +='\n\\begin{figure}\n\centering\n'

# Add the final \end{figure}
output += '\n\\end{figure}\n'

# Write the output to a new LaTeX file
with open('diagrams.tex', 'w') as f:
    f.write(output)
f.close()


# Open the LaTeX file
with open('diagrams.tex', 'r') as f:
    content = f.read()

# Find all occurrences of \begin{subfigure} and \end{subfigure}
subfigures = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)

# Initialize the output string
output = '\n'

# Initialize a counter for the number of subfigures
counter = 0

# Iterate over the subfigures
for subfigure in subfigures:
    # Add the subfigure to the output
    output += subfigure + '\n'

    # Increment the counter
    counter += 1

    # If this is the 4th, 8th, 12th,... subfigure, add a \end{figure} and a \begin{figure}
    if counter % 10 == 0 and counter!= len(subfigures):
        output += '\\clearpage\n'

# Write the output to a new LaTeX file
with open('diagrams.tex', 'w') as f:
    f.write(output)
f.close()
