# Topology and PCSPs

Tools for computing homological properties of Hom complex of relational structures; it relies on Jakub Opršal's [```pcsptools```](https://github.com/jakub-oprsal/pcsptools) for all polymorphism computations.

## Installation

It is possible to install directly from GitHub:

```
python3 -m pip install git+https://github.com/gtasinato/topologytools
```

## Usage

In ```topology``` there are routines to compute multihomomorphisms between two structures and into a product of two structures:

```
from pcsptools import nae, onein
from topologytools import topology as tp

mhoms = tp.mhoms_generator(onein(3), nae(2)) # returns a generator iterating through multihomomorphisms
prod_mhoms = tp.mhom_product(onein(3), nae(2), nae(2)) # also returns a generator iterating through all multihomomorphisms

```

There is a ```ProdSimp_Complex``` class that computes the convex cells in the Hom complex (as polyhedral complex):

```
>>>from pcsptools import nae, Structure
>>>from topologytools import topology as tp

>>>test = Structure({0,1,2}, [(1,2,3),(2,3,1), (3,1,2)])
>>>x = tp.ProdSimp_Complex(test, nae(2)) # In this case a circle

>>>x.dim #dimension of x
1 
>>>x.euler # Euler characteristic
2 

```

In ```homology```, the class ```ChainComplex``` is defined:

```
from pcsptools import Structure, nae
from topologytools import homology as hm

t = Structure({0,1,2}, [(1,2,3),(2,3,1), (3,1,2)])

y = hm.ChainComplex(t, nae(2)) #can be initialized with two Stucture instances or a ProdSimp_Complex one

y.betti(1, coeff=0) # Betti number over the reals
1 
```
 - in ```utils.py``` there are some useful functions/subroutines

## TO-DO 

Here there are features I will slowly try to implement.

### Planned
These are ideas that are potentially feasible:

 - in ```topology```:
   - [ ] Compute only the split multihomomorphisms to the product of two targets
   - [ ] Automatically compute the closure of a collection of cells if one is given when creating a ```ProdSimp_Complex``` instance.
 - in ```homology```:
   - [ ] Compute integer homology
   - [ ] Decide existence of chain homotopy between maps over reals
   - [ ] Decide existence of chain homotopy between maps over finite fields
   - [ ] Decide existence of chain homotopy between maps over integers


### Pipedreams

Here is a list of features I personally would love to see implemented at some point. Not sure if it is ever going to happen though :)

 - [ ] Properly document functions/classes
 - [ ] Different functorial constructions, especially [this](https://arxiv.org/abs/2512.05120) form Beikmohammadi and Bulatov.
 - [ ] Compute the minion homomorphism explicitly.

