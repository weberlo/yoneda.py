from hom_functor import *
from cat_insts import *

WA = build_walking_arrow()
one = WA.find_obj_by_name('1')
two = WA.find_obj_by_name('2')
f = WA.find_mor_by_name('f')
id_1 = WA.find_mor_by_name('id_1')
id_2 = WA.find_mor_by_name('id_2')

def test_covariant():
    SC = SetCat()
    WA_1_x = build_covariant_hom_functor(WA, one, SC)
    print(WA_1_x.F_obj(one))
    print(WA_1_x.F_obj(two))
    print(WA_1_x.F_mor(f))
    print(WA_1_x.F_mor(id_1))
    print(WA_1_x.F_mor(id_2))


def test_contravariant():
    SC = SetCat()
    WA_x_1 = build_contravariant_hom_functor(WA, one, SC)
    print(WA_x_1.F_obj(one))
    print(WA_x_1.F_obj(two))
    print(WA_x_1.F_mor(f))
    print(WA_x_1.F_mor(id_1))
    print(WA_x_1.F_mor(id_2))


if __name__ == '__main__':
    # test_covariant()
    test_contravariant()
