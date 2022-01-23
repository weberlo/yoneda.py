from typing import Callable, TypeVar

from obj import Object
from morphism import Morphism
from category import Category
from util.symbol import Symbol

O = TypeVar('O')
M = TypeVar('M')

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

    @property
    def comp_rule(self) -> Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]:
        def res(f_op: Morphism[O, M], g_op: Morphism[O, M]) -> Morphism[O, M]:
            return self.cat.flip_mor(self.cat.comp_rule(self.cat.flip_mor(g_op), self.cat.flip_mor(f_op)))
        return res

    @property
    def flip_mor(self, f: Morphism[O, M]) -> Morphism[O, M]:
        return self.cat.flip_mor(f)
