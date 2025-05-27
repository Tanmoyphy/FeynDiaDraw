import re
import sys
from vertex import *

class Line:
    """
    Represents a sequence of connected vertices, forming a 'line' in a Feynman diagram.
    This class manages the order and connection of vertices.
    """
    def __init__(self):
        """
        Initializes an empty Line object.
        vertices: A list to store Vertex objects in sequence.
        open: A boolean flag indicating if the line has an open end (i.e., an external particle).
        """
        self.vertices = []
        self.open = False

    def __getitem__(self, index):
        """
        Allows accessing vertices by index, e.g., line[0].
        """
        return self.vertices[index]

    def __setitem__(self, index, value):
        """
        Allows setting vertices by index, e.g., line[0] = new_vertex.
        """
        self.vertices[index] = value

    def additem(self, v):
        """
        Adds a Vertex object 'v' to the line, attempting to place it in the correct
        position based on its field connections.
        If the vertex has an external field (starts with 'ext'), it's added to the beginning or end.
        Otherwise, it tries to connect to existing vertices based on field numbers.
        """

        if re.search('[a-zA-Z]', v.fields[0]):
            self.vertices.insert(0, v) 
            self.open = True
        elif re.search('[a-zA-Z]', v.fields[1]):
            self.vertices.append(v)
            self.open = True
        else:
            next_field_expected = str(int(v.fields[1]) + 1)
            prev_field_expected = str(int(v.fields[0]) - 1)
            
            i = 0
            found = False
            for w in self.vertices:
                if next_field_expected == w.fields[0]:
                    self.vertices.insert(i, v) 
                    found = True
                    break
                if prev_field_expected == w.fields[1]:
                    self.vertices.insert(i + 1, v) 
                    found = True
                    break
                i += 1
            if not found:
                self.vertices.append(v)

    def __iter__(self):
        """
        Allows iteration over the vertices in the line, e.g., for v in line: ...
        """
        return iter(self.vertices)

    def __len__(self):
        """
        Returns the number of vertices in the line, e.g., len(line).
        """
        return len(self.vertices) 

    def __contains__(self, v):
        """
        Checks if a given vertex 'v' is "connected" to any vertex already in the line.
        Connection is determined by field numbers (v.fields[0]-1 == w.fields[1] or v.fields[1]+1 == w.fields[0]).
        """
        print("") 
        print("trying to see if") 
        print(v.fields) 
        print("is connected to")
        for w in self.vertices:
            print(w.fields) 
        
        contained = False
        for w in self.vertices:
            try:
                if int(v.fields[0]) - 1 == int(w.fields[1]):
                    contained = True
                    break
            except ValueError:
                pass
            try:
                if int(v.fields[1]) + 1 == int(w.fields[0]):
                    contained = True
                    break
            except ValueError:
                pass
        
        return contained

    def __add__(self, line2):
        """
        Concatenates two Line objects, creating a new Line containing all vertices from both.
        """
        nline = Line()
        for v in self:
            nline.additem(v)
        for v in line2:
            nline.additem(v)
        return nline

