from category import *
from functor import *

def build_Z2():
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

    return Z2.finish()


class SetCat(Category):
    def __init__(self):
        pass

    def compose(self, f, g):
        assert f.tgt == g.src, f'source and target don\'t match: ({f}, {g})'
        # import pdb; pdb.set_trace()
        return Morphism(f.src, lambda x: g(f(x)), f.tgt, is_ident=f.is_ident and g.is_ident)


Z2 = build_Z2()
X = Z2.find('X')
zero = Z2.find('0')
one = Z2.find('1')

SC = SetCat()

def F_obj(A: 'Object[Z2]'):
    assert A == X
    return Object({zero, one}, SC)


def F_mor(f: 'Morphism[X, X]'):
    if f == zero:
        res = lambda S: {g >> zero for g in S}
    elif f == one:
        res = lambda S: {g >> one for g in S}
    else:
        assert False
    return Morphism(F_obj(f.src), res, F_obj(f.tgt), is_ident=f.is_ident)


CayleyF = Functor(Z2, SC, F_obj, F_mor)
print(CayleyF(X))
print(CayleyF(zero))
X_Set = CayleyF(X)
zero_Set = CayleyF(zero)
one_Set = CayleyF(one)
print(zero_Set >> one_Set)
print(zero_Set >> zero_Set)

# Z2 = build_Z2()
# zero = Z2.find('0')
# one = Z2.find('1')
# print(zero >> zero)
# print(zero >> one)
# print(one >> one)
# print(one >> one >> one)
