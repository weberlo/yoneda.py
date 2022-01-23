from typing import Generic, TypeVar, Any

from util.symbol import *

from obj import Object

O = TypeVar('O')
M = TypeVar('M')

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

