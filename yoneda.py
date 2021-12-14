from category import *
from functor import *
from hom_functor import *
from nat_trans import *

# TODO maybe there should be a singleton Set instance
SC = SetCat()

def build_yoneda_embed(C: Category, COpToSet: 'PresheafCat'):
    assert isinstance(COpToSet, PresheafCat)
    def F_obj(X: 'Object[C]'):
        fnor = build_contravariant_hom_functor(C, X, SC)
        return COpToSet.find(fnor)

    def F_mor(f: 'Morphism[X, Y]'):
        # TODO There's something not right about how we're building the
        # morphisms.  I'd recommend starting from scratch in this function.
        F = F_obj(f.src).sym
        G = F_obj(f.tgt).sym
        def eta(A):
            res = SetMorSym(lambda g: g >> f, f'· >> {f.sym}')
            return SC.find_mor(Morphism(F(A), res, G(A), is_ident=f.is_ident))
        res = PshMorSym(NatTrans(F, G, eta), f'· >> {f.sym}')
        return SC.find_mor(Morphism(F, res, G, is_ident=f.is_ident))

    return Functor(C, COpToSet, F_obj, F_mor)


class PshMorSym:
    def __init__(self, eta: 'NatTrans', s: str):
        self.eta = eta
        self.s = s

    def __call__(self, arg):
        return self.eta(arg)

    def __str__(self):
        return self.s

    def __repr__(self):
        return str(self)


class PresheafCat(Category):
    def __init__(self):
        super().__init__()

    def find(self, s: 'Any'):
        res = super().find(s)
        if res is not None:
            return res
        if isinstance(s, Functor):
            [res] = self.add_objs([s])
            return res
        else:
            assert False

#     def add_mors(self, mors: 'List[Morphism]'):
#         res = super().add_mors(mors)
#         return {self.find_mor(mor) for mor in res}

#     def find_mor(self, f: Morphism):
#         # TODO Whenever we have a new morphism, check that the composition rule
#         # still obeys laws.

#         # Determine whether this is a new morphism by enumerating inputs and checking outputs.
#         # Only frozen sets are hashable.
#         graph = frozenset((elt, f.sym.fn(elt)) for elt in f.src.sym)
#         self.mor_eval_cache.setdefault(graph, []).append(f)
#         res = self.mor_eval_cache[graph][0]
#         # assert f.is_ident == res.is_ident, 'inconsistent identity tags'
#         return res

#     def _comp_rule(self, f: Morphism, g: Morphism) -> Morphism:
#         fn = lambda x: g(f(x))
#         sym = SetMorSym(fn, f'({f}) >> ({g})', f)
#         res = Morphism(f.src, sym, f.tgt, is_ident=f.is_ident and g.is_ident)
#         return self.find_mor(res)

#     def find(self, s: 'Any'):
#         res = super().find(s)
#         if res is not None:
#             return res
#         if isinstance(s, Functor):
#             [res] = self.add_objs([s])
#             return res
#         # elif isinstance(s, NatTrans):
#         #     [res] = self.add_mors([s])
#         #     return res
#         else:
#             assert False
