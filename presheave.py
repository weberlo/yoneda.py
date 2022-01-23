from category import *
from functor import *
from nat_trans import *

# TODO We should be able to refactor the commonalities in Set and PshCat
Fn = Callable[[Any], Any]
Psh = Functor[CO, CM, set[Any], Fn]
PshObj = Object[Psh[CO, CM]]
PshNatTrans = NatTrans[CO, CM, set[Any], Fn]
PshMor = Morphism[Psh[CO, CM], PshNatTrans[CO, CM]]
SetMor = Morphism[set[Any], Fn]

class PshCat(Category[Psh[CO, CM], PshNatTrans[CO, CM]]):
    _local_graph_to_mor: \
        dict[tuple[PshObj[CO, CM], PshObj[CO, CM]],
             dict[frozenset[tuple[Object[CO], SetMor]], PshMor[CO, CM]]]
    base_cat: Category[CO, CM]
    set_cat: SetCat

    def __init__(self, C: Category[CO, CM], set_cat: SetCat):
        self._sym = Symbol(f'[{C} ⟶ {set_cat}]')
        self._objs = set()
        self._mors = set()
        self._hom = {}
        self._idents = {}
        self._local_graph_to_mor = {}
        self.base_cat = C
        self.set_cat = set_cat

    def compose(self, f: PshMor[CO, CM], g: PshMor[CO, CM]) -> PshMor[CO, CM]:
        eta1 = f.data
        eta2 = g.data
        def eta(X: Object[CO]) -> SetMor:
            return eta1(X) >> eta2(X)
        data = NatTrans(eta1.src, eta2.tgt, eta)
        name = f'({f}) >> ({g})'
        return self.find_mor_by_nat_trans(f.src, data, g.tgt, name)

    def find_obj_by_functor(self, F: Psh[CO, CM], name: str | None = None) -> PshObj[CO, CM]:
        for X in self.objs:
            # TODO This equality check is quite expensive.  We should cache it
            # similarly to Set.
            if X.data == F:
                return X
        assert name is not None, 'new object needs name'
        obj = Object(name, F)
        self.objs.add(obj)

        # Create identity morphism.
        def eta(X: Object[CO]) -> SetMor:
            F_X = F.obj_map(X)
            return self.set_cat.find_mor_by_fn(F_X, lambda x: x, F_X, name=f'id_({F_X})')
        ident_data = NatTrans(F, F, eta)
        self.find_mor_by_nat_trans(obj, ident_data, obj, name=f'id_({name})')

        return obj

    def find_mor_by_nat_trans(
            self,
            src: PshObj[CO, CM],
            nat_trans: PshNatTrans[CO, CM],
            tgt: PshObj[CO, CM],
            name: str | None = None) -> PshMor[CO, CM]:
        # TODO Whenever we have a new morphism, check that the composition rule
        # still obeys laws.
        assert src in self.objs, f'source {src} not in objects'
        assert tgt in self.objs, f'target {tgt} not in objects'
        F = src.data
        G = tgt.data
        assert F.src == G.src and F.tgt == G.tgt, 'incomparable functors'
        C = F.src
        domain = list(C.objs)
        image = [nat_trans(X) for X in domain]
        graph = frozenset(zip(domain, image))
        if (src, tgt) in self._local_graph_to_mor and graph in self._local_graph_to_mor[(src, tgt)]:
            # If we've already encountered the graph for this type signature,
            # return the previously encountered morphism.
            return self._local_graph_to_mor[(src, tgt)][graph]
        # Otherwise, this is a new morphism.
        assert name is not None, 'new morphism needs name'
        mor: PshMor[CO, CM] = Morphism(src, name, nat_trans, tgt, cat=self)
        self.mors.add(mor)
        self._hom.setdefault((src, tgt), set()).add(mor)
        self._local_graph_to_mor.setdefault((src, tgt), {})[graph] = mor
        # TODO this could be a method in `Category`
        def is_ident(f: SetMor) -> bool:
            return f.src == f.tgt and self.set_cat.idents[f.src] == f
        if all(map(is_ident, image)):
            # Note this is only valid because we're using list equality and not
            # set equality.  If it were set equality, we would know it's a
            # bijection, but not an identity function.
            self.idents[src] = mor
        return mor
