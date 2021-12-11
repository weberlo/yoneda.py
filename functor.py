from category import *
from util import *

class Functor:
    def __init__(self, C: Category, D: Category, F_obj, F_mor):
        self.F_obj = F_obj
        self.F_mor = F_mor

        if CHECK_LAWS:
            for X in C.objs:
                F_id_X = F_mor(C.idents[X])
                id_FX = D.idents[F_obj(X)]
                assert F_id_X == id_FX, 'identity law violated'

            for f in C.mors:
                for g in C.mors:
                    if f.tgt == g.src:
                        F_f = F_mor(f)
                        F_g = F_mor(g)
                        F_f_g = F_mor(f >> g)
                        assert (F_f >> F_g) == F_f_g, 'composition law violated'

        # If this is a functor into a dynamically constructed category, it would
        # be good to initialize any of those morphisms before we pick out any
        # particular ones.  For example, if we have Cayley's functor for group
        # categories, then we might not recognize (· >> 1) >> (· >> 1) as (· >>
        # 2) if we haven't initialized that morphism.
        for obj in C.objs:
            F_obj(obj)
        for mor in C.mors:
            F_mor(mor)


    def __call__(self, arg):
        if isinstance(arg, Object):
            return self.F_obj(arg)
        elif isinstance(arg, Morphism):
            return self.F_mor(arg)
        elif isinstance(arg, Category):
            assert False, 'unimplemented'
        else:
            assert False, 'unimplemented'
