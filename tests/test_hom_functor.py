from instances.functor.hom_functor import *
from instances import *

WA = build_walking_arrow()
one = WA.find_obj_by_name('1')
two = WA.find_obj_by_name('2')
f = WA.find_mor_by_name('f')
id_1 = WA.find_mor_by_name('id_1')
id_2 = WA.find_mor_by_name('id_2')

def test_covariant():
    SC = SetCat()
    WA_1_x = build_covariant_hom_functor(WA, one, SC)
    print(WA_1_x.obj_map(one))
    print(WA_1_x.obj_map(two))
    print(WA_1_x.mor_map(f))
    print(WA_1_x.mor_map(id_1))
    print(WA_1_x.mor_map(id_2))


def test_contravariant():
    SC = SetCat()
    WA_x_1 = build_contravariant_hom_functor(WA, one, SC)
    print(WA_x_1.obj_map(one))
    print(WA_x_1.obj_map(two))
    print(WA_x_1.mor_map(f.op).str_with_type())
    print(WA_x_1.mor_map(id_1.op).str_with_type())
    print(WA_x_1.mor_map(id_2.op).str_with_type())


if __name__ == '__main__':
    test_covariant()
    test_contravariant()
