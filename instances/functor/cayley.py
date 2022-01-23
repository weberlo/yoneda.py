from category import *
from functor import *
from instances import *

def build_cayley_functor(G: Category[O, M], SC: SetCat) -> Functor[O, M, set[Any], Fn]:
    [X] = G.objs

    def obj_map(A: Object[O]) -> SetObj:
        assert A == X
        SC_obj = G.hom(A, A)
        return SC.find_obj_by_set(SC_obj, name=str(SC_obj))

    def mor_map(f: Morphism[O, M]) -> SetMor:
        name = f'· >> {f.sym}'
        data: Callable[[Morphism[O, M]], Morphism[O, M]] = lambda g: g >> f
        F_src = obj_map(f.src)
        F_tgt = obj_map(f.tgt)
        return SC.find_mor_by_fn(F_src, data, F_tgt, name=name)
    return Functor(G, SC, obj_map, mor_map)

