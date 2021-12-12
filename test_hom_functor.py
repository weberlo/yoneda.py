from hom_functor import *
from cat_insts import *

WA = build_walking_arrow()
one = WA.find('1')
two = WA.find('2')
f = WA.find('f')
id_1 = WA.find('id_1')
id_2 = WA.find('id_2')

def test_covariant():
    SC = SetCat()
    WA_1_x = build_covariant_hom_functor(WA, one, SC)
    print(WA_1_x(one))
    print(WA_1_x(two))
    print(WA_1_x(f))
    print(WA_1_x(id_1))
    print(WA_1_x(id_2))


def test_contravariant():
    SC = SetCat()
    WA_x_1 = build_contravariant_hom_functor(WA, one, SC)
    print(WA_x_1(one))
    print(WA_x_1(two))
    print(WA_x_1(f))
    print(WA_x_1(id_1))
    print(WA_x_1(id_2))


if __name__ == '__main__':
    test_contravariant()
