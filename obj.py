from typing import Generic, TypeVar, Any
from util.symbol import Symbol

O = TypeVar('O')

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
