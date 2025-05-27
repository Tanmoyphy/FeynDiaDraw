import sys

class propagator:
    """
    Represents a propagator (line) in a Feynman diagram, connecting two vertices.
    """
    def __init__(self, element):
        """
        Initializes a Propagator object from an XML element (assuming element is a BeautifulSoup/lxml element).
        Extracts 'from' vertex, 'to' vertex, field type, and an ID.
        """
        try:
            self.vfrom = element.find("from").text
            self.vto = element.find("to").text
            self.fromto = {self.vfrom, self.vto}
            self.field = element.find("field").text
            self.id = element.find("id").text
        except Exception as e: 
            print(f"Error while defining propagator object: {e}", file=sys.stderr)

    def texprint(self, file, particledict, shape=""):
        """
        Writes a LaTeX-formatted string for the propagator to the given file.
        This is typically used for drawing Feynman diagrams with packages like `feynmf`.

        Args:
            file: The file object to write to.
            particledict: A dictionary mapping field names to their LaTeX representations.
            shape: An optional string to specify the shape of the propagator line in LaTeX.
                   If empty, a default shape is used.
        """
        if shape == "":
            file.write("{} -- [ {} ] {},\n ".format(self.vfrom, particledict[self.field], self.vto))
        else:
            file.write("{} -- [ {},{} ] {},\n".format(self.vfrom, particledict[self.field], shape, self.vto))

