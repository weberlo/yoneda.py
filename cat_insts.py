from category import *

def build_Zn(n: int):
    Zn = Category()

    [X] = Zn.add_objs(['X'])

    mors = [Morphism(X, str(i), X) for i in range(n)]
    # 0 is the identity
    mors[0].is_ident = True
    mors = Zn.add_mors(mors)

    comp_dict = {}
    for a in mors:
        for b in mors:
            comp_dict[(a, b)] = mors[(int(a.sym) + int(b.sym)) % n]
    def comp_rule(f: Morphism, g: Morphism):
        return comp_dict[(f, g)]
    Zn.add_comp_rule(comp_rule)

    return Zn


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
