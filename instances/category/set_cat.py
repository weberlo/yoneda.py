from typing import Callable, Any

from obj import Object
from morphism import Morphism
from category import Category

Fn = Callable[[Any], Any]
SetObj = Object[set[Any]]
SetMor = Morphism[set[Any], Fn]

class SetCat(Category[set[Any], Fn]):
    local_graph_to_mor: dict[tuple[SetObj, SetObj], dict[frozenset[tuple[Any, Any]], SetMor]]

    def __init__(self):
        self._objs = set()
        self._mors = set()
        self._hom = {}
        self._idents = {}
        self.local_graph_to_mor = {}

    def _comp_rule(self, f: SetMor, g: SetMor) -> SetMor:
        def data(x: Any) -> Any:
            return g.data(f.data(x))
        name = f'({f}) >> ({g})'
        return self.find_mor_by_fn(f.src, data, g.tgt, name)

    def find_obj_by_set(self, data: set[Any], name: str | None = None) -> SetObj:
        for X in self.objs:
            if X.data == data:
                return X
        assert name is not None, 'new object needs name'
        obj = Object(name, data)
        self.objs.add(obj)
        # Create identity morphism.
        self.find_mor_by_fn(obj, lambda x: x, obj, name=f'id_({name})')
        return obj

    def find_mor_by_fn(self, src: SetObj, fn: Fn, tgt: SetObj, name: str | None = None) -> SetMor:
        # TODO Whenever we have a new morphism, check that the composition rule
        # still obeys laws.
        assert src in self.objs, f'source {src} not in objects'
        assert tgt in self.objs, f'target {tgt} not in objects'
        # Determine whether this is a new morphism by enumerating inputs and checking outputs.
        # Convert to list to determinize the order.
        domain = list(src.data)
        image = [fn(elt) for elt in domain]
        codomain = tgt.data
        assert set(image).issubset(codomain), f"function ({name}) from {src} doesn't map onto subset of {tgt}: image={set(image)}"
        # Note: need frozen sets, in order to be hashable.
        graph = frozenset(zip(domain, image))
        if (src, tgt) in self.local_graph_to_mor and graph in self.local_graph_to_mor[(src, tgt)]:
            # If we've already encountered the graph for this type signature,
            # return the previously encountered morphism.
            return self.local_graph_to_mor[(src, tgt)][graph]
        # Otherwise, this is a new morphism.
        assert name is not None, 'new morphism needs name'
        mor: SetMor = Morphism(src, name, fn, tgt, cat=self)
        self.mors.add(mor)
        self._hom.setdefault((src, tgt), set()).add(mor)
        self.local_graph_to_mor.setdefault((src, tgt), {})[graph] = mor
        if domain == image and src == tgt:
            # Note this is only valid because we're using list equality and not
            # set equality.
            self.idents[src] = mor
        return mor
