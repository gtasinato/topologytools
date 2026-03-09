from pcsptools import *

def fix(key):
    if isinstance(key, int):
        return (key,)
    if isinstance(key, tuple):
        return key
    raise IndexError("Key should be either int or tuple, not a {}".format(type(key)))

def cofix(value, partial_sol = None):
    res = []
    if partial_sol != None:
        res = partial_sol.copy()
       
    for v in value:
        if isinstance(v, tuple):
            res += cofix(v, partial_sol = res)
        else:
            res.append(v)
    return res

def validate(relation, condition):
    return any(condition in r for r in relation.relations)

def mmorph_validator(source, target, mmorph):
    for relation in source.relations:
        for constraint in relation:
            controls = [mmorph[fix(id)] for id in constraint]
            if not all(validate(target, c) for c in product(*controls)):
                return False
    return True

def powerset(iterable):
    "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def compose(mhom, poly):
    return {fix(key): [poly[value] for value in mhom[key]] for key in mhom}

def mhoms_from_homs(source, target):
    homomorphisms = list(polymorphisms(source, target, 1))
    for fs in powerset(homomorphisms):
        mhom = { (i,): [] for i in source.domain}
        for key in mhom:
            mhom[key] = list({f[key] for f in fs})
        if mmorph_validator(source, target, mhom):
            yield mhom

def mhoms_from_sets(source, target):
    aux = powerset(target.domain)
    for s in product(aux, repeat=len(source.domain)):
        mhom = {fix(candidate[0]) : list(candidate[1]) for candidate in zip(source.domain, s)}
        if mmorph_validator(source, target, mhom):
            yield mhom

def mhom_product(source, a, b, method="sets"):
    base = map(fix, source.domain)
    mhoms_a = mhoms_generator(source, a, method) if isinstance(a, Structure) else a 
    mhoms_b = mhoms_generator(source, b, method) if isinstance(b, Structure) else b
    tupler = lambda x: tuple(cofix(x))
    for m_a, m_b in product(mhoms_a, mhoms_b):
        yield {key: list(map(tupler, product(m_a[key], m_b[key]))) for key in base}

def mhoms_generator(source, target, method="sets"):
    if method == "homs":
        yield from mhoms_from_homs(source, target)
    else:
        yield from mhoms_from_sets(source, target)

def hyperedge(r):
    shift = lambda x, i: tuple(x[(j+i)%r] for j in range(r))
    return Structure(set(range(r)), [shift(tuple(range(r)), i) for i in range(r)])


