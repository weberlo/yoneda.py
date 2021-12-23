from typing import TypeVar
# from enum import Enum as _Enum

# class Enum(_Enum):
#     @classmethod
#     def export_to(cls, namespace: dict[str, object]):
#         namespace.update(cls.__members__)


E = TypeVar('E')
class BiDict(dict[E, E]):
    def __setitem__(self, key: E, value: E):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict[E, E].__setitem__(self, key, value)
        dict[E, E].__setitem__(self, value, key)

    def __delitem__(self, key: E):
        dict[E, E].__delitem__(self, self[key])
        dict[E, E].__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict[E, E].__len__(self) // 2
