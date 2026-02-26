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

