from category import *
from functor import *
from cat_insts import *

def build_cayley_functor(G: Category[O, M], SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    [X] = G.objs

    def F_obj(A: Object[O]) -> SetObj:
        assert A == X
        SC_obj = G.hom[(A, A)]
        return SC.find_obj_by_set(SC_obj, name=str(SC_obj))

    def F_mor(f: Morphism[O, M]) -> SetMor:
        name = f'· >> {f.sym}'
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: g >> f
        F_src = F_obj(f.src)
        F_tgt = F_obj(f.tgt)
        return SC.find_mor_by_fn(F_src, data, F_tgt, name=name)
    return Functor(G, SC, F_obj, F_mor)

