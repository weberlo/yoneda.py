from enum import Enum

from category import *
from util import *

class Variance(Enum):
    Covariant = 0
    Contravariant = 1
# Variance.export_to(globals())


CO = TypeVar('CO')
CM = TypeVar('CM')
DO = TypeVar('DO')
DM = TypeVar('DM')

class Functor(Generic[CO, CM, DO, DM]):
    def __init__(
            self,
            C: Category[CO, CM],
            D: Category[DO, DM],
            obj_map: Callable[[Object[CO]], Object[DO]],
            mor_map: Callable[[Morphism[CO, CM]], Morphism[DO, DM]],
            variance: Variance):
        self.src = C
        self.tgt = D
        self.obj_map = obj_map
        self.mor_map = mor_map
        self.variance = variance

        for X in C.objs:
            id_X = C.idents[X]
            F_id_X = mor_map(C.idents[X])
            FX = obj_map(X)
            id_FX = D.idents[obj_map(X)]
            assert F_id_X == id_FX, f'identity law violated F(id_({X})) == F({id_X}) == {F_id_X} != id_(F({X})) == id_({FX}) == {id_FX}'

        for f in C.mors:
            for g in C.mors:
                match self.variance:
                    case Variance.Covariant if f.tgt == g.src:
                        F_f = mor_map(f)
                        F_g = mor_map(g)
                        F_f_g = mor_map(f >> g)
                        assert (F_f >> F_g) == F_f_g, f'covariant composition law violated:\n  (({F_f}) >> ({F_g})) == {F_f >> F_g} != {F_f_g}'
                    case Variance.Contravariant if f.tgt == g.src:
                        F_f = mor_map(f)
                        F_g = mor_map(g)
                        F_f_g = mor_map(f >> g)
                        assert (F_g >> F_f) == F_f_g, f'contravariant composition law violated:\n  (({F_g}) >> ({F_f})) == {F_g >> F_f} != {F_f_g}'

        # TODO: Do we still need this if we're checking the laws above?  We're
        # calling obj_map and mor_map on all of the objects, it looks like.
        # If this is a functor into a dynamically constructed category (e.g.,
        # Set), it would be good to initialize any of those morphisms before we
        # pick out any particular ones.  For example, if we have Cayley's
        # functor for group categories, then we might not recognize (· >> 1) >>
        # (· >> 1) as (· >> 2) if we haven't initialized that morphism.
        for obj in C.objs:
            obj_map(obj)
        for mor in C.mors:
            mor_map(mor)

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, Functor)
        F = self
        G: Functor[CO, CM, DO, DM] = other
        assert F.src == G.src and F.tgt == G.tgt  # type: ignore
        # First, check objects are mapped to the same place.
        C = self.src
        for X in C.objs:
            if F.obj_map(X) != G.obj_map(X):
                return False
        # Then check morphisms are mapped to the same place
        for f in C.mors:
            if F.mor_map(f) != G.mor_map(f):
                return False
        return True

    # TODO I'd love to have this functionality but typechecking can't determine
    # which side of the sum the result lies on, even though it's clearly
    # deducible.  This leads to expressions like F(f) >> F(g) not typechecking,
    # because it thinks the operands *could* be objects.
    # def __call__(self, arg : Object[CO] | Morphism[CO, CM]):
    #     if isinstance(arg, Object):
    #         return self.obj_map(arg)
    #     else:
    #         return self.mor_map(arg)
