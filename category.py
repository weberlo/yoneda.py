from util import *

# TODO will this name fuck with python?
class Object:
    def __init__(self, sym, cat):
        self.sym = sym
        self.cat = cat

    def __str__(self):
        if isinstance(self.sym, frozenset):
            return f'{set(self.sym)}'
        return f'{self.sym}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.sym)

    def __eq__(self, other):
        if not isinstance(other, Object):
            return False
        return self.cat == other.cat and self.sym == other.sym


class Morphism:
    def __init__(self, src, sym, tgt, is_ident=False):
        self.src = src
        self.sym = gen_symbol(sym)
        self.tgt = tgt
        assert src.cat == tgt.cat, f'mismatched categories for {src} and {tgt}'
        self.cat = src.cat
        self.is_ident = is_ident
        # Print out binding with type, and add parentheses if there are any
        # spaces in the symbol name.
        sym_str = str(sym)
        sym_str = f'({sym_str})' if ' ' in sym_str else sym_str
        print(f'Let {sym_str}: {src} ⟶ {tgt}.')

    def __rshift__(self, other):
        return self.src.cat.compose(self, other)

    def __call__(self, arg):
        return self.sym(arg)

    def __str__(self):
        # return f'{self.src} -({self.sym})-> {self.tgt}'
        return f'{self.sym}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, Morphism):
            return False
        return self.cat == other.cat and self.src == other.src and self.sym == other.sym and self.tgt == other.tgt and self.is_ident == other.is_ident


# TODO check for when composition rule is violated
class Category:
    # objs: Set[Object]
    # mors: Set[Morphism]
    # hom: Dict[(Object, Object), Set[Morphism]]
    # idents: Dict[objs, mors]

    def __init__(self):
        self.objs = set()
        self.mors = set()
        self.hom = {}
        self.idents = {}

    def add_objs(self, new_objs: 'List[str]'):
        new_objs = [Object(gen_symbol(obj), self) for obj in new_objs]
        self.objs = self.objs.union(set(new_objs))
        # Return handles to new objects.
        return new_objs

    def add_mors(self, mors: 'List[Morphism]'):
        # First add any new objects.
        mor_objs = set(mor.src for mor in mors).union(set(mor.tgt for mor in mors))
        new_objs = mor_objs - self.objs
        self.add_objs(new_objs)
        # Then add new morphisms.
        self.mors = self.mors.union(mors)
        for a in self.objs:
            for b in self.objs:
                a_b_mors = set(filter(lambda m: m.src == a and m.tgt == b, mors))
                # Append morphisms.
                self.hom[(a, b)] = self.hom.setdefault((a, b), set()).union(a_b_mors)
                if a == b:
                    # Identity check
                    has_ident = False
                    for mor in a_b_mors:
                        if mor.is_ident:
                            assert not has_ident, f'multiple identity morphisms for {a}'
                            has_ident = True
                            self.idents[a] = mor
                    assert has_ident, f'no identity morphism for {a}'
        return mors

    def _add_mors(self, mors: 'List[Morphism]'):
        # Method to be overriden by subclasses.
        return mors

    def add_comp_rule(self, comp_rule: 'Fn[(Morphism, Morphism), Morphism]'):
        assert not hasattr(self, 'comp_rule'), 'composition rule already defined'
        self._comp_rule = comp_rule
        # Check associativity of composition rule.
        for f in self.mors:
            for g in self.mors:
                if f.tgt != g.src:
                    continue
                for h in self.mors:
                    if g.tgt != h.src:
                        continue
                    assert (f >> g) >> h == f >> (g >> h), f'associativity of composition violated: ({f} >> {g}) >> {h} == {f} >> ({g} >> {h})'

    def compose(self, f, g):
        assert f.tgt == g.src, f'source and target don\'t match: ({f}, {g})'
        assert hasattr(self, '_comp_rule'), 'no composition rule defined'
        return self._comp_rule(f, g)

    def find(self, s: 'Any'):
        # First search objects.
        for X in self.objs:
            if X.sym == s:
                return X
        # Then search morphisms.
        for f in self.mors:
            if f.sym == s:
                return f
        return None

    def __str__(self):
        return f'objs: {self.objs},\nmors: {self.mors}'

    def __repr__(self):
        return str(self)


#########################################################################
# We need special definitions for Set, since it's an infinite category. #
#########################################################################

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
        # TODO Whenever we have a new morphism, check that the composition rule
        # still obeys laws.

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
