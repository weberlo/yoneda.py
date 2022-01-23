from typing import Callable, Generic, TypeVar, Any
import itertools

from symbol import *
from util import BiDict

O = TypeVar('O')
M = TypeVar('M')

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

    @property
    def op(self) -> 'Morphism[O, M]':
        assert self.cat is not None, "can't flip morphisms without being situated in a category"
        return self.cat.flip_mor(self)

    def __str__(self):
            return f'{self.sym}'

    def str_with_type(self):
        return f'{self.src} -({self.sym})-> {self.tgt}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, Morphism)
        f = self
        g: Morphism[O, M] = other
        return f.src == g.src \
            and f.sym == g.sym \
            and f.data == g.data \
            and f.tgt == g.tgt \
            and f.cat == g.cat \

    def set_cat(self, cat: 'Category[O, M]'):
        assert self.cat is None, f'category already defined for morphism {self}'
        self.cat = cat

    def __rshift__(self, other: 'Morphism[O, M]') -> 'Morphism[O, M]':
        assert self.cat == other.cat, \
            f'mismatched categories {self} ∈ {self.cat}({self.src}, {self.tgt}) and {other} ∈ {other.cat}({other.src}, {other.tgt}) in composition'
        assert self.cat is not None, "category hasn't been set"
        return self.cat.compose(self, other)


from abc import ABC, abstractmethod
# TODO check for when composition rule is violated
class Category(ABC, Generic[O, M]):
    _sym: Symbol
    _objs: set[Object[O]]
    _mors: set[Morphism[O, M]]
    _hom: dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]]
    _idents: dict[Object[O], Morphism[O, M]]
    _op: 'Category[O, M]'
    _flip_mor_dict: BiDict[Morphism[O, M]]

    @property
    def sym(self) -> Symbol:
        return self._sym

    @property
    def objs(self) -> set[Object[O]]:
        return self._objs

    @property
    def mors(self) -> set[Morphism[O, M]]:
        return self._mors

    @property
    def hom(self) -> Callable[[Object[O], Object[O]], set[Morphism[O, M]]]:
        def res(X: Object[O], Y: Object[O]):
            return self._hom[(X, Y)]
        return res

    @property
    def idents(self) -> dict[Object[O], Morphism[O, M]]:
        return self._idents

    @abstractmethod
    def compose(self, f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        assert False

    @property
    def op(self) -> 'Category[O, M]':
        return self._op

    def flip_mor(self, f: Morphism[O, M]) -> Morphism[O, M]:
        """Return morphism in the opposite category."""
        if f not in self._flip_mor_dict:
            # The only way it wouldn't be in the dictionary is if it hasn't been
            # created in the opposite category yet, so we must be converting a
            # regular morphism to an opposite morphism.  All other cases are
            # handled by the default case after the `if`.
            op_mor_name = f.sym.name
            if len(op_mor_name) > 1:
                op_mor_name = f'({op_mor_name})'
            op_mor_name = f'{op_mor_name}ᵒᵖ'
            self._flip_mor_dict[f] = Morphism(f.tgt, op_mor_name, f.data, f.src, self.op)
        return self._flip_mor_dict[f]

    def __str__(self):
        return str(self.sym)

    def __repr__(self):
        return str(self)


class FinCat(Category[O, M]):
    _comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]

    def __init__(
            self,
            objs: set[Object[O]],
            mors: set[Morphism[O, M]],
            comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]],
            name: str | None = None):
        super().__init__()
        self._objs = objs
        for mor in mors:
            mor.set_cat(self)
        self._mors = mors
        self._comp_rule = comp_rule
        self._hom = self._gen_hom_set()
        self._idents = self._find_idents()
        self._check_comp_rule()
        if name is None:
            name = gen_fresh('C')
        self._sym = Symbol(name)

    def _gen_hom_set(self) -> dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]]:
        hom: dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]] = {}
        for X in self.objs:
            for Y in self.objs:
                hom[(X, Y)] = set(filter(lambda m: m.src == X and m.tgt == Y, self.mors))
        return hom

    def _find_idents(self) -> dict[Object[O], Morphism[O, M]]:
        idents: dict[Object[O], Morphism[O, M]] = {}
        for X in self.objs:
            for f in self.hom(X, X):
                is_ident = True
                # f >> g =? g
                for g in self.mors:
                    if g.src == X and (f >> g) != g:
                        is_ident = False
                        break
                # g >> f =? g
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
            for (f, g, h) in itertools.product(self.hom(X, Y), self.hom(Y, Z), self.hom(Z, W)):
                assert (f >> g) >> h == f >> (g >> h), f'associativity of composition violated: ({f} >> {g}) >> {h} != {f} >> ({g} >> {h})'

    def compose(self, f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        assert f.tgt == g.src, f"target of ({f.str_with_type()}) doesn't match source of ({g.str_with_type()})"
        return self._comp_rule(f, g)

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

    @property
    def objs(self) -> set[Object[O]]:
        return self._objs

    @property
    def mors(self) -> set[Morphism[O, M]]:
        return self._mors

    @property
    def hom(self) -> Callable[[Object[O], Object[O]], set[Morphism[O, M]]]:
        def res(X: Object[O], Y: Object[O]):
            return self._hom[(X, Y)]
        return res

    @property
    def idents(self) -> dict[Object[O], Morphism[O, M]]:
        return self._idents

    @property
    def sym(self) -> Symbol:
        return self._sym

    @property
    def op(self) -> 'Category[O, M]':
        return self._op


#########################################################################
# We need special definitions for Set, since it's an infinite category. #
#########################################################################

Fn = Callable[[Any], Any]
SetObj = Object[set[Any]]
SetMor = Morphism[set[Any], Fn]

class SetCat(Category[set[Any], Fn]):
    # _objs: set[Object[set[Any]]]
    # _mors: set[Morphism[set[Any], Fn]]
    # _hom: dict[tuple[Object[set[Any]], Object[set[Any]]], set[Morphism[set[Any], Fn]]]
    # _idents: dict[Object[set[Any]], Morphism[set[Any], Fn]]
    _local_graph_to_mor: dict[tuple[SetObj, SetObj], dict[frozenset[tuple[Any, Any]], SetMor]]

    def __init__(self):
        self._objs = set()
        self._mors = set()
        self._hom = {}
        self._idents = {}
        self._local_graph_to_mor = {}
        self._sym = Symbol('𝒮𝑒𝑡')
        self._op = OpCat(self)

    def compose(self, f: SetMor, g: SetMor) -> SetMor:
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
        if (src, tgt) in self._local_graph_to_mor and graph in self._local_graph_to_mor[(src, tgt)]:
            # If we've already encountered the graph for this type signature,
            # return the previously encountered morphism.
            return self._local_graph_to_mor[(src, tgt)][graph]
        # Otherwise, this is a new morphism.
        assert name is not None, 'new morphism needs name'
        mor: SetMor = Morphism(src, name, fn, tgt, cat=self)
        self.mors.add(mor)
        self._hom.setdefault((src, tgt), set()).add(mor)
        self._local_graph_to_mor.setdefault((src, tgt), {})[graph] = mor
        if domain == image and src == tgt:
            # Note this is only valid because we're using list equality and not
            # set equality.
            self.idents[src] = mor
        return mor

    @property
    def objs(self) -> set[SetObj]:
        return self._objs

    @property
    def mors(self) -> set[SetMor]:
        return self._mors

    @property
    def hom(self) -> Callable[[SetObj, SetObj], set[SetMor]]:
        def res(X: SetObj, Y: SetObj):
            return self._hom[(X, Y)]
        return res

    @property
    def idents(self) -> dict[SetObj, SetMor]:
        return self._idents

    @property
    def sym(self) -> Symbol:
        return self._sym

    @property
    def op(self) -> 'Category[set[Any], Fn]':
        return self._op


class OpCat(Category[O, M]):
    """The opposite category of an input category.

    This class automatically tracks changes to the input by virtue of always
    dispatching to the input category's data.  That is, the class merely
    rearranges the directions of morphisms before passing them to the input
    category's morphism set, hom sets, composition rule, etc.
    """
    cat: Category[O, M]

    def __init__(self, cat: Category[O, M]):
        self.cat = cat
        self._sym = Symbol(cat.sym.name + 'ᵒᵖ')

    @property
    def objs(self):
        return self.cat.objs

    @property
    def mors(self):
        return set(map(self.cat.flip_mor, self.cat.mors))

    @property
    def hom(self):
        def _hom(X: Object[O], Y: Object[O]) -> set[Morphism[O, M]]:
            return set(map(self.cat.flip_mor, self.cat.hom(Y, X)))
        return _hom

    @property
    def idents(self):
        return {X: self.cat.flip_mor(self.cat.idents[X]) for X in self.objs}

    def compose(self, f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        # These are morphisms in the opposite cat, so we notate them as such.
        f_op = f
        g_op = g
        # Flip the morphisms, use the base category's composition rule with the
        # arguments reversed, then flip the resulting morphism.
        return self.cat.flip_mor(self.cat.compose(self.cat.flip_mor(g_op), self.cat.flip_mor(f_op)))

    def flip_mor(self, f: Morphism[O, M]) -> Morphism[O, M]:
        return self.cat.flip_mor(f)

    @property
    def sym(self) -> Symbol:
        return self._sym

    @property
    def op(self) -> Category[O, M]:
        return self.cat
