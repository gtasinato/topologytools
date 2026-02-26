from itertools import combinations
from topologytools.utils import powerset, mmorph_validator, cofix, fix 

def mhoms_generator(source, target):
    aux = powerset(target.domain)
    for s in product(aux, repeat=len(source.domain)):
        mhom = {fix(candidate[0]) : list(candidate[1]) for candidate in zip(source.domain, s)}
        if mmorph_validator(source, target, mhom):
            yield mhom

def mhom_product(source, a, b):
    base = map(fix, source.domain)
    mhoms_a = mhoms_generator(source, a) if isinstance(a, Structure) else a 
    mhoms_b = mhoms_generator(source, b) if isinstance(b, Structure) else b
    tupler = lambda x: tuple(cofix(x))
    for m_a, m_b in product(mhoms_a, mhoms_b):
        yield {key: list(map(tupler, product(m_a[key], m_b[key]))) for key in base}

class ProdSimp_Complex:
    """Class computing Hom(a, b). The two mandatory args are the wo structures, optionally can provide a dictionary cells = {dim : [list of multihomomorphisms]}
    """
    def __init__(self, t, a, cells = None):
        self._left_structure = t
        self._right_structure = a
        if cells is not None:
            self._cells = cells
        else:
            cells = {}
            mhoms = mhoms_generator(self.left_structure, self.right_structure)

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
