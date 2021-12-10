from util import *

# TODO will this name fuck with python?
class Object:
    def __init__(self, sym, cat):
        self.sym = sym
        self.cat = cat

    def __str__(self):
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

    def __rshift__(self, other):
        return self.src.cat.compose(self, other)

    def __str__(self):
        return f'{self.src} -({self.sym})-> {self.tgt}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, Morphism):
            return False
        return self.cat == other.cat and self.src == other.src and self.sym == other.sym and self.tgt == other.tgt and self.is_ident == other.is_ident


# Use `CatBuilder`
class Category:
    # objs: Set[str]
    # mors: Dict[(objs, objs), Set[Any]]
    # comp: Dict[(mors, mors), mors]
    # ident: Dict[objs, mors]

    def compose(self, f, g):
        assert f.tgt == g.src, f'source and target don\'t match: ({f}, {g})'
        return self.comp[(f, g)]

    def find(self, s):
        # first search objects
        for X in self.objs:
            if X.sym == s:
                return X
        # then search morphisms
        for f in self.mors:
            if f.sym == s:
                return f
        assert False, f'no such object or morphism {s}'

    def __str__(self):
        return f'objs: {self.objs},\nmors: {self.mors}'

    def __repr__(self):
        return str(self)


class CatBuilder:
    def __init__(self):
        self.cat = Category()

    def add_objs(self, objs):
        objs = [Object(gen_symbol(obj), self.cat) for obj in objs]
        self.cat.objs = objs
        return objs

    def add_mors(self, mors):
        assert hasattr(self.cat, 'objs'), 'must define objects before morphisms'
        self.cat.mors = mors
        hom = {}
        idents = {}
        for a in self.cat.objs:
            for b in self.cat.objs:
                if a == b:
                    a_b_mors = list(filter(lambda m: m.src == a and m.tgt == b, mors))
                    hom[(a, b)] = a_b_mors
                    # identity check
                    has_ident = False
                    for mor in a_b_mors:
                        if mor.is_ident:
                            assert not has_ident, f'multiple identity morphisms for {a}'
                            has_ident = True
                            idents[a] = mor
                    assert has_ident, f'no identity morphism for {a}'
        self.cat.hom = hom
        self.cat.idents = idents

    def add_comp(self, comp):
        assert hasattr(self.cat, 'mors'), 'must define morphisms before composition'
        self.cat.comp = comp

    def finish(self):
        return self.cat

