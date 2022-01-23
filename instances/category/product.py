import itertools
from typing import TypeVar

from category import Category
from morphism import Morphism
from obj import Object

O1 = TypeVar('O1')
M1 = TypeVar('M1')
O2 = TypeVar('O2')
M2 = TypeVar('M2')
O = tuple[O1, O2]
M = tuple[M1, M2]

def prod(C: Category[O1, M1], D: Category[O2, M2]) -> Category[O, M]:
    objs = set()
    prod_obj_to_comps = {}
    for X in C.objs:
        for Y in D.objs:
            Z = Object(f'({X.sym} ⨉_{{{C.sym} ⨉_{{Cat}} {D.sym}}} {Y.sym})', (X.data, Y.data))
            prod_obj_to_comps[Z] = (X, Y)
            objs.add(Z)

    mors = set()
    prod_mor_to_comps = {}
    prod_comps_to_mor = {}
    for Z1, Z2 in itertools.product(objs, objs):
        (X1, Y1) = prod_obj_to_comps[Z1]
        (X2, Y2) = prod_obj_to_comps[Z2]
        for (f1, f2) in itertools.product(C.hom(X1, X2), D.hom(Y1, Y2)):
            f = Morphism(Z1, f'⟨{f1.sym}, {f2.sym}⟩', (f1.data, f2.data), Z2)
            prod_mor_to_comps[f] = (f1, f2)
            prod_comps_to_mor[(f1, f2)] = f
            mors.add(f)

    def comp_rule(f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        (f1, f2) = prod_mor_to_comps[f]
        (g1, g2) = prod_mor_to_comps[g]
        return prod_comps_to_mor[(f1 >> g1, f2 >> g2)]

    return Category(objs, mors, comp_rule, f'{C.sym} ⨉_{{Cat}} {D.sym}')


