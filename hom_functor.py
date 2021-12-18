from category import *
from functor import *
from cat_insts import *

def build_covariant_hom_functor(
        C: Category[O, M],
        A: Object[O],
        SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    def obj_map(X: Object[O]) -> SetObj:
        data = C.hom[(A, X)]
        name = str(data)
        return SC.find_obj_by_set(data, name=name)

    def mor_map(f: Morphism[O, M]) -> SetMor:
        # name = f'· >> {f}'
        name = f'{C}({A}, {f})'
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: g >> f
        F_src = obj_map(f.src)
        F_tgt = obj_map(f.tgt)
        return SC.find_mor_by_fn(F_src, data, F_tgt, name=name)

    return Functor(C, SC, obj_map, mor_map, Variance.Covariant)


def build_contravariant_hom_functor(
        C: Category[O, M],
        B: Object[O],
        SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    def obj_map(X: Object[O]) -> SetObj:
        data = C.hom[(X, B)]
        name = str(data)
        return SC.find_obj_by_set(data, name=name)

    def mor_map(f: Morphism[O, M]) -> SetMor:
        F_src = obj_map(f.src)
        F_tgt = obj_map(f.tgt)
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: f >> g
        # name = f'{f} >> ·'
        name = f'{C}({f}, {B})'
        # Note we've flipped the src and tgt.
        return SC.find_mor_by_fn(F_tgt, data, F_src, name=name)

    return Functor(C, SC, obj_map, mor_map, Variance.Contravariant)

