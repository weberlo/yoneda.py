from category import *
from functor import *
from cat_insts import *

def build_covariant_hom_functor(C: Category, A: 'Object[C]', SC: SetCat):
    def F_obj(X: 'Object[C]'):
        return SC.find(C.hom[(A, X)])

    def F_mor(f: 'Morphism[X, Y]'):
        res = SetMorSym(lambda g: g >> f, f'· >> {f.sym}')
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        return SC.find_mor(Morphism(F_src, res, F_tgt, is_ident=f.is_ident))

    return Functor(C, SC, F_obj, F_mor)


def build_contravariant_hom_functor(C: Category, B: 'Object[C]', SC: SetCat):
    def F_obj(X: 'Object[C]'):
        return SC.find(C.hom[(X, B)])

    def F_mor(f: 'Morphism[X, Y]'):
        res = SetMorSym(lambda g: f >> g, f'{f.sym} >> ·')
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        # Note we've flipped the src and tgt.
        return SC.find_mor(Morphism(F_tgt, res, F_src, is_ident=f.is_ident))

    return Functor(C, SC, F_obj, F_mor)

