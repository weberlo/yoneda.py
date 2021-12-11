from category import *
from functor import *
from cat_insts import *

def build_cayley_functor(G: Category, SC: SetCat):
    [X] = G.objs
    elts = G.mors

    def F_obj(A: 'Object[Z2]'):
        assert A == X
        return SC.find(set(elts))

    def F_mor(f: 'Morphism[X, X]'):
        res = SetMorSym(lambda g: g >> f, f'· >> {f.sym}', f)
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        return SC.find_mor(Morphism(F_src, res, F_tgt, is_ident=f.is_ident))
    return Functor(G, SC, F_obj, F_mor)

