from typing import Callable, Generic, TypeVar, Any
import itertools

from util.symbol import *
from util.collections import BiDict

from obj import Object
from morphism import Morphism

O = TypeVar('O')
M = TypeVar('M')

# TODO check for when composition rule is violated
class Category(Generic[O, M]):
    _objs: set[Object[O]]
    _mors: set[Morphism[O, M]]
    _hom: dict[tuple[Object[O], Object[O]], set[Morphism[O, M]]]
    _idents: dict[Object[O], Morphism[O, M]]
    _comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]
    _sym: Symbol
    _op: 'Category[O, M]'
    _flip_mor_dict : BiDict[Morphism[O, M]]

    def __init__(
            self,
            objs: set[Object[O]],
            mors: set[Morphism[O, M]],
            comp_rule: Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]],
            name: str | None = None):
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
        self._op = OpCat(self)
        self._flip_mor_dict = BiDict()

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
            for (f, g, h) in itertools.product(self.hom(X, Y), self.hom(Y, Z), self.hom(Z, W)):
                assert (f >> g) >> h == f >> (g >> h), f'associativity of composition violated: ({f} >> {g}) >> {h} != {f} >> ({g} >> {h})'

    def compose(self, f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        assert f.tgt == g.src, f"target of ({f.str_with_type()}) doesn't match source of ({g.str_with_type()})"
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

    def find_mor_by_data(self, src: Object[O], data: M, tgt: Object[O]):
        return self.find_mor(lambda f: f.src == src and f.data == data and f.tgt == tgt)

    def find_mor(self, pred: Callable[[Morphism[O, M]], bool]) -> Morphism[O, M]:
        res = None
        for f in self.mors:
            if pred(f):
                assert res is None, 'multiple morphisms satisfying predicate'
                res = f
        assert res is not None, 'no morphism satisfying predicate'
        return res

    def flip_mor(self, f: Morphism[O, M]) -> Morphism[O, M]:
        """Return morphism in the opposite category."""
        if f not in self._flip_mor_dict:
            # It could only not be in the dictionary if it hasn't been created
            # in the opposite category yet, so we must be converting a regular
            # morphism to an opposite morphism.  All other cases are handled by
            # the default case after the `if`.
            op_mor_name = f.sym.name
            if len(op_mor_name) > 1:
                op_mor_name = f'({op_mor_name})'
            op_mor_name = f'{op_mor_name}ᵒᵖ'
            self._flip_mor_dict[f] = Morphism(f.tgt, op_mor_name, f.data, f.src, self.op)
        return self._flip_mor_dict[f]

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
    def comp_rule(self) -> Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]:
        return self._comp_rule

    @property
    def sym(self) -> Symbol:
        return self._sym

    @property
    def op(self) -> 'Category[O, M]':
        return self._op

    def __str__(self):
        # return f'objs: {self.objs},\nmors: {self.mors}'
        return str(self.sym)

    def __repr__(self):
        return str(self)


# Must import this after declaring `Category`, so `OpCat`s constructor can be
# used in `Category`s constructor.
from op_cat import OpCat
