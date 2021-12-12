from category import *
from functor import *
from cat_insts import *

def build_covariant_hom_functor(C: Category, X: 'Object[C]', SC: SetCat):
    def F_obj(Y: 'Object[C]'):
        return SC.find(C.hom[(X, Y)])

    def F_mor(f: 'Morphism[Y, Z]'):
        res = SetMorSym(lambda g: g >> f, f'· >> {f.sym}', f)
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        return SC.find_mor(Morphism(F_src, res, F_tgt, is_ident=f.is_ident))

    return Functor(C, SC, F_obj, F_mor)

