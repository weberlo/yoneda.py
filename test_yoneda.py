from hom_functor import *
from cat_insts import *
from yoneda import *
from presheave import *

def test_walking_arrow():
    WA = build_walking_arrow()
    one = WA.find_obj_by_name('1')
    two = WA.find_obj_by_name('2')
    f = WA.find_mor_by_name('f')
    id_1 = WA.find_mor_by_name('id_1')
    id_2 = WA.find_mor_by_name('id_2')

    SC = SetCat()
    PshC = PshCat[None, None](SC)
    H = build_yoneda_embed(WA, PshC)

    print(H.obj_map(one))
    print(H.obj_map(two))
    print(H.mor_map(f))
    print(H.mor_map(id_1))
    print(H.mor_map(id_2))


def test_nontriv_comp():
    C = build_nontriv_comp()
    X = C.find_obj_by_name('X')
    Y = C.find_obj_by_name('Y')
    Z = C.find_obj_by_name('Z')
    f = C.find_mor_by_name('f')
    g = C.find_mor_by_name('g')

    Set = SetCat()
    PshC = PshCat[None, None](Set)
    H = build_yoneda_embed(C, PshC)

    print(H.obj_map(X))
    print(H.obj_map(Y))
    print(H.obj_map(Z))
    print(H.mor_map(f))
    print(H.mor_map(g))


if __name__ == '__main__':
    # test_walking_arrow()
    test_nontriv_comp()
