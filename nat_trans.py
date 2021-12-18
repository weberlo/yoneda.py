from category import *
from debug import DebugBlock
from functor import *

class NatTrans(Generic[CO, CM, DO, DM]):
    src: Functor[CO, CM, DO, DM]
    tgt: Functor[CO, CM, DO, DM]
    eta: Callable[[Object[CO]], Morphism[DO, DM]]

    # A family of morphisms in the target category between two functors
    def __init__(
            self,
            F: Functor[CO, CM, DO, DM],
            G: Functor[CO, CM, DO, DM],
            eta: Callable[[Object[CO]], Morphism[DO, DM]]):
        self.src = F
        self.tgt = G
        self.eta = eta
        C = F.src

        for X in C.objs:
            g = eta(X)
            assert F.obj_map(X) == g.src and G.obj_map(X) == g.tgt, "natural transformation doesn't map between objects in the image of F and G"

        for f in C.mors:
            F_f = F.mor_map(f)
            G_f = G.mor_map(f)
            eta_X = eta(f.src)
            eta_Y = eta(f.tgt)
            # TODO The casing on variance is a code smell.  We should be able to
            # build an "opposite category" construction that tracks the original
            # category and produces morphisms according to the original
            # category.
            match (F.variance, G.variance):
                case (Variance.Covariant, Variance.Covariant):
                    assert F_f >> eta_Y == eta_X >> G_f, 'naturality condition violated'
                case (Variance.Covariant, Variance.Contravariant):
                    assert False
                case (Variance.Contravariant, Variance.Covariant):
                    assert False
                case (Variance.Contravariant, Variance.Contravariant):
                    assert F_f >> eta_X == eta_Y >> G_f, 'naturality condition violated'

    def __call__(self, arg: Object[CO]) -> Morphism[DO, DM]:
        return self.eta(arg)
