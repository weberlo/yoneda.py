from typing import Callable, Generic, TypeVar, Any
import itertools

from symbol import *

O = TypeVar('O')
M = TypeVar('M')
K = TypeVar('K')

class Object(Generic[O]):
    sym: Symbol
    data: O

    def __init__(self, name: str, data: O):
        self.sym = Symbol(name)
        self.data = data

    def __str__(self):
        return str(self.sym)

    def __repr__(self):
        return str(self.sym)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: Any):
        assert isinstance(other, Object)
        return self.sym == other.sym


class Morphism(Generic[O, M]):
    src: Object[O]
    sym: Symbol
    data: M
    tgt: Object[O]
    cat: 'Category[O, M] | None'

    def __init__(
            self,
            src: Object[O],
            name: str,
            data: M,
            tgt: Object[O],
            cat: 'Category[O, M] | None' = None):
        self.src = src
        self.sym = Symbol(name)
        self.data = data
        self.tgt = tgt
        self.cat = cat
        # Print out binding with type, and add parentheses if there are any
        # spaces in the symbol name.
        name_str = f'({name})' if ' ' in name else name
        print(f'Let {name_str}: {src} ⟶ {tgt}.')

    def __str__(self):
        # return f'{self.src} -({self.sym})-> {self.tgt}'
        return f'{self.sym}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, Morphism)
        return self.src == other.src \
            and self.sym == other.sym \
            and self.data == other.data \
            and self.tgt == other.tgt \
            and self.cat == other.cat

    def set_cat(self, cat: 'Category[O, M]'):
        assert self.cat is None, f'category already defined for morphism {self}'
        self.cat = cat

    def __rshift__(self, other: 'Morphism[O, M]') -> 'Morphism[O, M]':
        assert self.cat == other.cat, 'mismatched categories in composition'
        assert self.cat is not None, 'category not set'
        return self.cat.compose(self, other)


# TODO check for when composition rule is violated
class Category(Generic[O, M]):
    objs: set[Object[O]]
    mors: set[Morphism[O, M]]
    comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]
    hom: dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]]
    idents: dict[Object[O], Morphism[O, M]]

    def __init__(
            self,
            objs: set[Object[O]],
            mors: set[Morphism[O, M]],
            comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]):
        self.objs = objs
        for mor in mors:
            mor.set_cat(self)
        self.mors = mors
        self.comp_rule = comp_rule
        self.hom = self._gen_hom_set()
        self.idents = self._find_idents()
        self._check_comp_rule()

    def _gen_hom_set(self) -> dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]]:
        hom: dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]] = {}
        for X in self.objs:
            for Y in self.objs:
                hom[(X, Y)] = set(filter(lambda m: m.src == X and m.tgt == Y, self.mors))
        return hom

    def _find_idents(self) -> dict[Object[O], Morphism[O, M]]:
        idents: dict[Object[O], Morphism[O, M]] = {}
        for X in self.objs:
            for f in self.hom[(X, X)]:
                is_ident = True
                # f >> g ?= g
                for g in self.mors:
                    if g.src == X and (f >> g) != g:
                        is_ident = False
                        break
                # g >> f ?= g
                for g in self.mors:
                    if g.tgt == X and (g >> f) != g:
                        is_ident = False
                        break
                if is_ident:
                    assert X not in idents, f'multiple identities {idents[X]} and {f} for {X}'
                    idents[X] = f
            assert X in idents, f'no identity morphism for {X}'
        return idents

    def _check_comp_rule(self):
        """Check associativity of composition rule."""
        for (X, Y, Z, W) in itertools.product(self.objs, self.objs, self.objs, self.objs):
            for (f, g, h) in itertools.product(self.hom[(X, Y)], self.hom[(Y, Z)], self.hom[(Z, W)]):
                assert (f >> g) >> h == f >> (g >> h), f'associativity of composition violated: ({f} >> {g}) >> {h} != {f} >> ({g} >> {h})'

    def compose(self, f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        assert f.tgt == g.src, f'source and target don\'t match: ({f}, {g})'
        return self.comp_rule(f, g)

    def find_obj_by_name(self, name: str):
        return self.find_obj(lambda X: X.sym.name == name)

    def find_obj(self, pred: Callable[[Object[O]], bool]) -> Object[O]:
        res = None
        for X in self.objs:
            if pred(X):
                assert res is None, 'multiple objects satisfying predicate'
                res = X
        assert res is not None, 'no object satisfying predicate'
        return res

    def find_mor_by_name(self, name: str):
        return self.find_mor(lambda f: f.sym.name == name)

    def find_mor(self, pred: Callable[[Morphism[O, M]], bool]) -> Morphism[O, M]:
        res = None
        for f in self.mors:
            if pred(f):
                assert res is None, 'multiple morphisms satisfying predicate'
                res = f
        assert res is not None, 'no morphism satisfying predicate'
        return res

    def __str__(self):
        return f'objs: {self.objs},\nmors: {self.mors}'

    def __repr__(self):
        return str(self)


#########################################################################
# We need special definitions for Set, since it's an infinite category. #
#########################################################################

# class SetMorSym:
#     def __init__(self, fn: 'Fn', s: str):
#         self.fn = fn
#         self.s = s

#     def __call__(self, arg):
#         return self.fn(arg)

#     def __str__(self):
#         return self.s

#     def __repr__(self):
#         return str(self)

Fn = Callable[[Any], Any]
SetObj = Object[set[Any]]
SetMor = Morphism[set[Any], Fn]

class SetCat(Category[set[Any], Fn]):
    graph_to_mor: dict[frozenset[tuple[Any, Any]], SetMor]

    def __init__(self):
        self.objs = set()
        self.mors = set()
        self.hom = {}
        self.idents = {}
        self.graph_to_mor = {}

    def comp_rule(self, f: SetMor, g: SetMor) -> SetMor:
        def data(x: Any) -> Any:
            return g.data(f.data(x))
        name = f'({f}) >> ({g})'
        return self.find_mor_by_fn(f.src, data, f.tgt, name)

    def find_obj_by_set(self, data: set[Any], name: str | None = None) -> SetObj:
        for X in self.objs:
            if X.data == data:
                return X
        assert name is not None, 'new object needs name'
        obj = Object(name, data)
        self.objs.add(obj)
        # Create identity morphism.
        self.find_mor_by_fn(obj, lambda x: x, obj, name=f'id_{name}')
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
        assert set(image).issubset(codomain), f"function from {src} doesn't map onto subset of {tgt}"
        # Note: need frozen sets, in order to be hashable.
        graph = frozenset(zip(domain, image))
        if graph in self.graph_to_mor:
            # If we've already encountered the graph, return the previously encountered morphism.
            return self.graph_to_mor[graph]
        # Otherwise, this is a new morphism.
        assert name is not None, 'new morphism needs name'
        mor: SetMor = Morphism(src, name, fn, tgt, cat=self)
        self.mors.add(mor)
        self.hom.setdefault((src, tgt), set()).add(mor)
        self.graph_to_mor[graph] = mor
        if domain == image:
            # Note this is only valid because we're using list equality and not
            # set equality.
            self.idents[src] = mor
        return mor
