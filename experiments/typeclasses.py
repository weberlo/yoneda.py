from abc import ABC
from cmath import exp
from dataclasses import dataclass
from typing import Any, Callable, Generic, Protocol, TypeVar, get_args, get_type_hints

def pubfields(cls: type) -> list[str]:
    return list(filter(lambda x: not x.startswith('_'), vars(cls)))


class TypeClass(ABC): pass

V = TypeVar('V')
class TypeClassDispatcher(Generic[V]):
    ty_cls: TypeClass
    fn_name: str
    impls: dict[type, V]

    def __init__(self, ty_cls: TypeClass, fn_name: str):
        self.ty_cls = ty_cls
        self.fn_name = fn_name
        self.impls = {}

    def add_impl(self, inst: type, impl: V):
        assert inst not in self.impls, \
            f'Implementation of {self.ty_cls.__name__}.{self.fn_name} for {inst} already exists'
        for i in self.impls:
            assert not isinstance(inst, i), \
                f'Overlapping instances not supported.  Adding {inst} when {inst} ⋞ {i}.'
            assert not isinstance(i, inst), \
                f'Overlapping instances not supported.  Adding {inst} when {i} ⋞ {inst}.'
        self.impls[inst] = impl

    def __getitem__(self, ty: type):
        return self.impls[ty]

    def __str__(self):
        return f'TyClsDispatcher(ty_cls={self.ty_cls}, fn_name={self.fn_name})'


from inspect import signature

TYPECLASS_DECL_REGISTRY: dict[TypeClass, dict[str, type]] = {}
TYPECLASS_FN_REGISTRY: dict[TypeClass, dict[type, dict[str, Any]]] = {}
def typeclass(ty_cls: type) -> type:
    pub_defs = dict((f, signature(getattr(ty_cls, f))) for f in pubfields(ty_cls))
    TYPECLASS_DECL_REGISTRY[ty_cls] = pub_defs
    TYPECLASS_FN_REGISTRY[ty_cls] = {f: TypeClassDispatcher(ty_cls, f) for f in pubfields(ty_cls)}
    return ty_cls


# TODO Metaclass instead of ABC + decorator combo?
# TODO Incorporate `Protocol` somehow?
M = TypeVar('M')
@typeclass
class Monoid(TypeClass, Generic[M]):
    def unit() -> M: ...
    def mappend(a: M, b: M) -> M: ...
    # unit = M
    # mappend = Callable[[M, M], M]


# C = TypeVar('C')
# T = TypeVar('T')
# def ayy(a : Monoid[C]) -> T:
#     import pdb; pdb.set_trace()
#     return None

# ayy[int]()
# ayy[float]()

def instance(ty_cls: type, cls: type, **defs: dict[str, Any]):
    # print(ty_cls)
    # Ensure the instance adheres to the typeclass interface.
    req_defs = TYPECLASS_DECL_REGISTRY[ty_cls]
    assert defs.keys() == req_defs.keys(), \
        f"{ty_cls.__name__} instance {cls.__name__} doesn't adhere to interface:\n" \
            f"    {list(sorted(defs.keys()))} ≠ {list(sorted(req_defs.keys()))}"
    # Add a namespace for the current instance.
    # namespace = {}
    # TYPECLASS_FN_REGISTRY[ty_cls][cls] = namespace
    for fn_name, fn in defs.items():
        expected_ty = req_defs[fn_name]
        exp_arg_tys = list(map(lambda p: p.annotation, expected_ty.parameters.values()))
        exp_ret_ty = expected_ty.return_annotation
        # Wrap the function with assertions that validate the type signature.
        # NOTE: Python has late binding, so we need to make the closure
        # explicit to ensure distinct variables are being captured at each
        # loop iteration.
        def mk_wrapper(ty_cls, cls, fn_name, fn, exp_arg_tys, exp_ret_ty):
            def wrapper(*args, **kwargs):
                # print(list(map(get_type_hints, args)))
                # print(ty_cls)
                # print(cls)
                # print(fn_name)
                # print(fn)
                assert len(args) == len(exp_arg_tys), \
                    f'got args {args}; expected args of type {exp_arg_tys}'
                assert not kwargs, 'keyword args unsupported'
                for (arg, exp_arg_ty) in zip(args, exp_arg_tys):
                    # TODO check types
                    pass
                res = fn(*args, **kwargs)
                # TODO assert return type is correct
                return res
            return wrapper
        TYPECLASS_FN_REGISTRY[ty_cls][fn_name].add_impl(cls, mk_wrapper(ty_cls, cls, fn_name, fn, exp_arg_tys, exp_ret_ty))
        # namespace[fn_name] = wrapper


L = TypeVar('L')
@dataclass
class List(Generic[L]): pass
@dataclass
class Nil(List[L]): pass
@dataclass
class Cons(List[L]):
    head: L
    tail: List[L]

def list_mappend(l1: List[L], l2: List[L]) -> List[L]:
    match l1:
        case Nil(): return l2
        case Cons(v, rest): return Cons(v, list_mappend(rest, l2))

instance(Monoid, List, unit=Nil, mappend=list_mappend)



def list_range(n: int) -> List[int]:
    res = Nil()
    for i in reversed(range(n)):
        res = Cons(i, res)
    return res


def list_sum(l: List[int]) -> int:
    match l:
        case Nil(): return 0
        case Cons(n, rest): return n + list_sum(rest)




# Register primitive list type as a monoid.
def list_mappend(l1: list[L], l2: list[L]) -> list[L]:
    return l1 + l2
instance(Monoid, list, unit=lambda: [], mappend=list_mappend)


# import pdb; pdb.set_trace()

class UnitSingleton:
    def __init__(self):
        # L = TypeVar('L')
        # self.impls = {int: 0, list[L]: []}
        # TODO support generics
        self.impls = {int: 0, list[int]: []}

    def __getitem__(self, ty: type):
        return self.impls[ty]

# unit = UnitSingleton()
# print(unit[int])
# print(unit[list[int]])

# list_unit = []
# list_mappend = lambda p: p[0].append(p[1])

# assert list_sum(list_range(3)) == sum(range(3))

def tc_open(ty_cls: TypeClass):
    for fn_name in TYPECLASS_DECL_REGISTRY[ty_cls].keys():
        assert fn_name not in globals(), \
            f"Can't open typeclass namespace {ty_cls.__name__}.  " \
                f'"{fn_name}" is already defined.'
        globals()[fn_name] = TYPECLASS_FN_REGISTRY[ty_cls][fn_name]

def tc_close(ty_cls: TypeClass):
    for fn_name, fn in TYPECLASS_FN_REGISTRY[ty_cls].items():
        # If the binding hasn't been changed since `tc_open`, remove it.
        if globals()[fn_name] == fn:
            del globals()[fn_name]

tc_open(Monoid)

l1 = Cons(1, Cons(2, Nil()))
l2 = Cons(3, Cons(4, Nil()))
print(unit[List]())
print(mappend[List](unit[List](), unit[List]()))
print(mappend[List](unit[List](), Cons(0, Nil())))

print(unit[list]())
print(mappend[list](unit[list](), [3]))
# print(mappend[List](unit[List], mappend[List](l1, l2)))

tc_close(Monoid)

try:
    print(unit[List]())
    assert False, "`unit` shouldn't be defined anymore"
except:
    pass
