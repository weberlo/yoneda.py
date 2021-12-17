from category import *
from functor import *
from cat_insts import *

def build_covariant_hom_functor(
        C: Category[O, M],
        A: Object[O],
        SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    def F_obj(X: Object[O]) -> SetObj:
        data = C.hom[(A, X)]
        name = str(data)
        return SC.find_obj_by_set(data, name=name)

    def F_mor(f: Morphism[O, M]) -> SetMor:
        name = f'· >> {f.sym}'
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: g >> f
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        return SC.find_mor_by_fn(F_src, data, F_tgt, name=name)

    return Functor(C, SC, F_obj, F_mor, Variance.Covariant)


def build_contravariant_hom_functor(
        C: Category[O, M],
        B: Object[O],
        SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    def F_obj(X: Object[O]) -> SetObj:
        data = C.hom[(X, B)]
        name = str(data)
        return SC.find_obj_by_set(data, name=name)

    def F_mor(f: Morphism[O, M]) -> SetMor:
        name = f'{f.sym} >> ·'
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: f >> g
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        # Note we've flipped the src and tgt.
        return SC.find_mor_by_fn(F_tgt, data, F_src, name=name)

    return Functor(C, SC, F_obj, F_mor, Variance.Contravariant)

