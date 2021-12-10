import category

class NatTrans:
    # A family of morphisms in the target category between two functors
    def __init__(
            self,
            F: 'Functor[C, D]',
            G: 'Functor[C, D]',
            eta: 'Dict[X : Object[C], FX -- f -- GX : Morphism[D]]'):
        C = F.src

        for X in C.objs:
            g = eta[X]
            assert F(X) == g.src and G(X) == g.tgt, 'natural transformation doesn\'t map between objects in the image of F and G'

        for f in C.mors:
            F_f = F(f)
            G_f = G(f)
            eta_X = eta[f.src]
            eta_Y = eta[f.tgt]
            assert F_f >> eta_Y == eta_X >> G_f, 'naturality condition violated'
