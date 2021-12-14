from category import *
from functor import *

class NatTrans:
    # A family of morphisms in the target category between two functors
    def __init__(
            self,
            F: 'Functor[C, D]',
            G: 'Functor[C, D]',
            eta: 'Fn[X : Object[C], FX -- f -- GX : Morphism[D]]'):
        self.eta = eta
        C = F.src

        for X in C.objs:
            g = eta(X)
            print(g)
            print(X)
            print(F(X))
            print(G(X))
            assert F(X) == g.src and G(X) == g.tgt, 'natural transformation doesn\'t map between objects in the image of F and G'

        for f in C.mors:
            F_f = F(f)
            G_f = G(f)
            eta_X = eta(f.src)
            eta_Y = eta(f.tgt)
            assert F_f >> eta_Y == eta_X >> G_f, 'naturality condition violated'

    def __call__(self, arg):
        assert isinstance(arg, Object), 'Can only apply natural transformations to objects'
        return self.eta(arg)
