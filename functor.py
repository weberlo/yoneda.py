from enum import Enum

from category import *
from util import *

class Variance(Enum):
    Covariant = 0
    Contravariant = 1

CO = TypeVar('CO')
CM = TypeVar('CM')
DO = TypeVar('DO')
DM = TypeVar('DM')

class Functor(Generic[CO, CM, DO, DM]):
    def __init__(
            self,
            C: Category[CO, CM],
            D: Category[DO, DM],
            F_obj: Callable[[Object[CO]], Object[DO]],
            F_mor: Callable[[Morphism[CO, CM]], Morphism[DO, DM]],
            variance: Variance):
        self.src = C
        self.tgt = D
        self.F_obj = F_obj
        self.F_mor = F_mor
        self.variance = variance

        for X in C.objs:
            F_id_X = F_mor(C.idents[X])
            id_FX = D.idents[F_obj(X)]
            assert F_id_X == id_FX, 'identity law violated'

        for f in C.mors:
            for g in C.mors:
                match self.variance:
                    case Variance.Covariant if f.tgt == g.src:
                        F_f = F_mor(f)
                        F_g = F_mor(g)
                        F_f_g = F_mor(f >> g)
                        assert (F_f >> F_g) == F_f_g, f'covariant composition law violated:\n  (({F_f}) >> ({F_g})) == {F_f >> F_g} != {F_f_g}'
                    case Variance.Contravariant if f.tgt == g.src:
                        F_f = F_mor(f)
                        F_g = F_mor(g)
                        F_f_g = F_mor(f >> g)
                        assert (F_g >> F_f) == F_f_g, f'contravariant composition law violated:\n  (({F_g}) >> ({F_f})) == {F_g >> F_f} != {F_f_g}'

        # TODO: Do we still need this if we're checking the laws above?  We're
        # calling F_obj and F_mor on all of the objects, it looks like.
        # If this is a functor into a dynamically constructed category (e.g.,
        # Set), it would be good to initialize any of those morphisms before we
        # pick out any particular ones.  For example, if we have Cayley's
        # functor for group categories, then we might not recognize (· >> 1) >>
        # (· >> 1) as (· >> 2) if we haven't initialized that morphism.
        for obj in C.objs:
            F_obj(obj)
        for mor in C.mors:
            F_mor(mor)

    # TODO I'd love to have this functionality but typechecking can't determine
    # which side of the sum the result lies on, even though it's clearly
    # deducible.  This leads to expressions like F(f) >> F(g) not typechecking,
    # because it thinks the operands *could* be objects.
    # def __call__(self, arg : Object[CO] | Morphism[CO, CM]):
    #     if isinstance(arg, Object):
    #         return self.F_obj(arg)
    #     else:
    #         return self.F_mor(arg)
