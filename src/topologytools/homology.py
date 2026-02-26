from functools import cache
import numpy as np
import galois
from itertools import combinations
from utils import compose
from topology import ProdSimp_Complex

class ChainComplex(ProdSimp_Complex):
    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(*args)
        elif len(args) == 1:
            assert isinstance(args[0], ProdSimp_Complex), "Not a valid type: expected ProdSimp_Complex recieved {}".format(type(args[0]))
            self.__dict__ = args[0].__dict__
        else:
            raise TypeError("Wrong number of inputs.")


    @cache
    def bd_matrix(self, d, coeff = 2):
        """Computing boundary matrix from d to d-1 with coeff in GF(coeff) 
        (coeff = 0 reals, coeff=1 integers)"""
        flag = (coeff ==0 or coeff ==1)

        if not flag:
            GF = galois.GF(coeff)
    
        if d<0 or d>self.dim+1:
            return np.zeros(1) if flag else GF.Zeros(1)
        if d == 0:
            return np.zeros(len(self.vertices)) if flag else GF.Zeros(len(self.vertices))
        if d == self.dim +1:
            return np.zeros((len(self.cells[d-1]), 1)) if flag else GF.Zeros((len(self.cells[d-1]), 1))
        basis_s = self.cells[d]
        basis_t = self.cells[d-1]
        m = [[0 for _ in basis_s] for _ in basis_t]
        product_sign = 0 
        # a is a multihomomorphism; e is the element in a and value is the subset of b associated to it
        for j, a in enumerate(basis_s):
            for e, value in a.items():
                if len(value) == 1:
                    continue               
                product_sign = (product_sign + len(value) - 1) %2
                
                
                # Sign adjustment since combinations takes faces starting from last vertex.
                sign = len(value)
                #Run through all the multihomomorphism obtained by dropping one element, keeping track of the sign
                for v in combinations(value, len(value)-1):
                    temp = a.copy()
                    sign = (sign + 1) %2
                    temp[e] = list(v)
                    
                    i = basis_t.index(temp)
                    m[i][j] = 1 if (product_sign + sign ) % 2 == 0 else -1 if flag else coeff -1
                    
        return m if coeff == 1 else np.array(m) if flag else GF(m)

    @cache
    def betti(self, d, coeff = 0):
    """The Betti numebr in dimension d on GF(coeff) (0 for reals/floats, 1 for ints)."""    
        c = 0 if (coeff == 0 or coeff == 1) else coeff
        m_upper = self.bd_matrix(d+1, coeff = c)
        m_lower = self.bd_matrix(d, coeff=c)
        rk_upper = 0 if not m_upper.any() else np.linalg.matrix_rank(m_upper)
        rk_lower = 0 if not m_lower.any() else np.linalg.matrix_rank(m_lower)
        dim = 0 if d not in self.cells else len(self.cells[d])

        return dim - rk_lower - rk_upper

class ChainMap:
    def __init__(self, source, target, map, coeff=2):
        assert source.left_structure == target.left_structure, "Complexes are not compatible"
        self._source = source
        self._target = target
        self._coeff = coeff

        if coeff !=2:
            raise TypeError("Only gf(2) implemented for the moment.")
        
        GF = galois.GF(coeff)

        maps = {}
        for dim in range(max(source.dim, target.dim)+1):
            try:
                j = len(source.cells[dim])
            except KeyError:
                j = 1
            try:
                i = len(target.cells[dim])
            except KeyError:
                i = 1
            maps[dim] = GF.Zeros((i, j))

        for dim in range(min(source.dim, target.dim) +1):
            basis_s = source.cells[dim]
            basis_t = target.cells[dim]
            for j, a in enumerate(basis_s):
                i = basis_t.index(compose(a, map))
                maps[dim][i][j] = 1
            
            
        self._maps= {dim: GF(m) for dim, m in maps.items()}

    @property
    def coeff(self):
        """The coeff property."""
        return self._coeff

    @property
    def source(self):
        """The source property."""
        return self._source

    @property
    def target(self):
        """The target property."""
        return self._target

    @property
    def maps(self):
        """The maps property."""
        return self._maps
    @property
    def dim(self):
        """The dim property."""
        return max(self.source.dim, self.target.dim)

def chain_homotopy(source, target, coeff=2):
    flag = False
    
    return flag

if __name__ == "__main__":
    pass
