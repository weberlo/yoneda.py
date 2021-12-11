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
        print(f'Let {sym}: {src} ⟶ {tgt}.')

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
        new_objs = {Object(gen_symbol(obj), self) for obj in new_objs}
        self.objs = self.objs.union(new_objs)
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
                if a == b:
                    a_b_mors = list(filter(lambda m: m.src == a and m.tgt == b, mors))
                    # Append morphisms.
                    self.hom[(a, b)] = self.hom.setdefault((a, b), []) + a_b_mors
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


# class CatBuilder:
#     def __init__(self):
#         self.cat = Category()

#     def add_objs(self, objs):
#         objs = [Object(gen_symbol(obj), self.cat) for obj in objs]
#         self.cat.objs = objs
#         return objs

#     def add_mors(self, mors):
#         assert hasattr(self.cat, 'objs'), 'must define objects before morphisms'
#         self.cat.mors = mors
#         hom = {}
#         idents = {}
#         for a in self.cat.objs:
#             for b in self.cat.objs:
#                 if a == b:
#                     a_b_mors = list(filter(lambda m: m.src == a and m.tgt == b, mors))
#                     hom[(a, b)] = a_b_mors
#                     # identity check
#                     has_ident = False
#                     for mor in a_b_mors:
#                         if mor.is_ident:
#                             assert not has_ident, f'multiple identity morphisms for {a}'
#                             has_ident = True
#                             idents[a] = mor
#                     assert has_ident, f'no identity morphism for {a}'
#         self.cat.hom = hom
#         self.cat.idents = idents

#     def set_comp_rule(self, comp_rule: 'Fn[(Morphism, Morphism), Morphism]'):
#         assert not hasattr(self.cat, 'comp_rule'), 'composition rule already defined'
#         self._comp_rule = comp_rule

#     def finish(self):
#         return self.cat

