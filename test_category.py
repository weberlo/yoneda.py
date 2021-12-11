from category import *
from functor import *

def build_Z2():
    Z2 = Category()

    [X] = Z2.add_objs(['X'])

    zero = Morphism(X, '0', X, is_ident=True)
    one = Morphism(X, '1', X)
    [zero, one] = Z2.add_mors([zero, one])

    comp_dict = {
        (zero, zero): zero,
        (zero, one): one,
        (one, zero): one,
        (one, one): zero,
    }
    def comp_rule(f: Morphism, g: Morphism):
        return comp_dict[(f, g)]

    Z2.add_comp_rule(comp_rule)

    return Z2


class SetMorSym:
    def __init__(self, fn: 'Fn', s: str, mor: Morphism):
        self.fn = fn
        self.s = s
        self.mor = mor

    def __call__(self, arg):
        return self.fn(arg)

    def __str__(self):
        return self.s

    def __repr__(self):
        return str(self)


class SetCat(Category):
    def __init__(self):
        super().__init__()
        self.mor_eval_cache = {}

    def add_mors(self, mors: 'List[Morphism]'):
        res = super().add_mors(mors)
        return {self.find_mor(mor) for mor in res}

    def find_mor(self, f: Morphism):
        # Determine whether this is a new morphism by enumerating inputs and checking outputs.
        # Only frozen sets are hashable.
        graph = frozenset((elt, f.sym.fn(elt)) for elt in f.src.sym)
        self.mor_eval_cache.setdefault(graph, []).append(f)
        res = self.mor_eval_cache[graph][0]
        # assert f.is_ident == res.is_ident, 'inconsistent identity tags'
        return res

    def _comp_rule(self, f: Morphism, g: Morphism) -> Morphism:
        fn = lambda x: g(f(x))
        sym = SetMorSym(fn, f'({f}) >> ({g})', f)
        res = Morphism(f.src, sym, f.tgt, is_ident=f.is_ident and g.is_ident)
        return self.find_mor(res)

    def find(self, s: 'Any'):
        res = super().find(s)
        if res is not None:
            return res
        if isinstance(s, set):
            [res] = self.add_objs([frozenset(s)])
            return res
        elif isinstance(s, frozenset):
            [res] = self.add_objs([s])
            return res
        else:
            assert False


Z2 = build_Z2()
X = Z2.find('X')
zero = Z2.find('0')
one = Z2.find('1')

SC = SetCat()

def F_obj(A: 'Object[Z2]'):
    assert A == X
    return SC.find({zero, one})


def F_mor(f: 'Morphism[X, X]'):
    res = SetMorSym(lambda g: g >> f, f'· >> {f.sym}', f)
    F_src = F_obj(f.src)
    F_tgt = F_obj(f.tgt)
    return SC.find_mor(Morphism(F_src, res, F_tgt, is_ident=f.is_ident))


CayleyF = Functor(Z2, SC, F_obj, F_mor)

X_Set = CayleyF(X)
zero_S = CayleyF(zero)
one_S = CayleyF(one)

print(f'{zero >> one=}')
print(f'{one >> one=}')

print(f'{(zero_S >> one_S)=}')
print(f'{(one_S >> one_S)=}')
