SYMBOL_REGISTRY = set()
def gen_symbol(sym):
    assert sym not in SYMBOL_REGISTRY, 'symbol already used'
    SYMBOL_REGISTRY.add(sym)
    return sym


# TODO will this name fuck with python?
class Object:
    def __init__(self, obj, cat):
        self.obj = obj
        self.cat = cat

    def __str__(self):
        return f'{self.obj}'

    def __hash__(self):
        return hash(self.obj)


class Morphism:
    def __init__(self, src, elt, tgt, is_ident=False):
        self.src = src
        self.elt = gen_symbol(elt)
        self.tgt = tgt
        assert src.cat == tgt.cat, f'mismatched categories for {src} and {tgt}'
        self.is_ident = is_ident

    def __rshift__(self, other):
        return self.src.cat.compose(self, other)

    def __str__(self):
        return f'{self.src} --({self.elt})--> {self.tgt}'

    def __hash__(self):
        return hash(str(self))


class CatBuilder:
    class Category:
        # objs: Set[str]
        # mors: Dict[(objs, objs), Set[Any]]
        # comp: Dict[(mors, mors), mors]

        def compose(self, f, g):
            assert f.tgt == g.src, f'source and target don\'t match: ({f}, {g})'
            return self.comp[(f, g)]


    def __init__(self):
        self.cat = self.Category()

    def add_objs(self, objs):
        objs = [Object(gen_symbol(obj), self.cat) for obj in objs]
        self.cat.objs = objs
        return objs

    def add_mors(self, mors):
        assert hasattr(self.cat, 'objs'), 'must define objects before morphisms'
        self.cat.mors = mors
        hom = {}
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
                            pass
                    assert has_ident, f'no identity morphism for {a}'
        self.cat.hom = hom

    def add_comp(self, comp):
        assert hasattr(self.cat, 'mors'), 'must define morphisms before composition'
        self.cat.comp = comp

    def finish(self):
        return self.cat


Z2 = CatBuilder()

[X] = Z2.add_objs(['X'])

zero = Morphism(X, '0', X, is_ident=True)
one = Morphism(X, '1', X)
Z2.add_mors({zero, one})

Z2.add_comp({
    (zero, zero): zero,
    (zero, one): one,
    (one, zero): one,
    (one, one): zero,
})

Z2 = Z2.finish()

print(zero >> zero)
print(zero >> one)
print(one >> one)
print(one >> one >> one)
