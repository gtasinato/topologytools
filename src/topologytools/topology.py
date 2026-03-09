from itertools import combinations, product
from topologytools.utils import mhoms_generator 

class ProdSimp_Complex:
    """Class computing Hom(a, b). The two mandatory args are the wo structures, optionally can provide a dictionary cells = {dim : [list of multihomomorphisms]}
    """
    def __init__(self, t, a, cells = None, method="sets"):
        self._left_structure = t
        self._right_structure = a
        if cells is not None:
            self._cells = cells
        else:
            cells = {}
            mhoms = mhoms_generator(self.left_structure, self.right_structure, method=method)

            for m in mhoms:
                length = sum(len(value)-1 for value in m.values())
                if length not in cells.keys():
                    cells[length] = [m]
                else:
                    cells[length].append(m)
            self._cells = cells 
        self._dim = max(self._cells)


    @property
    def dim(self):
        """The dimension of Hom(a, b)"""
        return self._dim

    @property
    def left_structure(self):
        """The left structure in Hom(a, b)."""
        return self._left_structure

    @property
    def right_structure(self):
        """The right structure in Hom(a, b)."""
        return self._right_structure

    @property
    def cells(self):
        """The cells in Hom(a, b). Returns a dict with key the dimension and value the list of cells."""
        return self._cells
    
    @property
    def vertices(self):
        """The vertices in Hom(a, b)."""
        return self._cells[0]
   
    @property
    def euler(self):
        """The Euler characteristic of Hom(a, b)"""
        return sum((-1)**i * len(cells) for i, cells in self.cells.items())


if __name__ == "__main__":
    pass
