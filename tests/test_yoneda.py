from instances.functor.hom_functor import *
from instances import *
from instances.functor.yoneda import *
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
    id_X = C.find_mor_by_name('id_X')
    f = C.find_mor_by_name('f')
    g = C.find_mor_by_name('g')

    Set = SetCat()
    PshC = PshCat[None, None](Set)
    H = build_yoneda_embed(C, PshC)

    H_X = H.obj_map(X)
    H_Y = H.obj_map(Y)
    H_Z = H.obj_map(Z)
    H_f = H.mor_map(f)
    H_g = H.mor_map(g)
    H_fg = H.mor_map(f >> g)
    print(f'{H_X=}')
    print(f'{H_Y=}')
    print(f'{H_Z=}')
    print(f'{H_f=}')
    print(f'{H_g=}')
    print(H_f >> H_g)
    C_X_fg = (H_f >> H_g).data(X)
    print(C_X_fg)
    print(C_X_fg.data(id_X.op))
    C_Y_f = H_f.data(Y)
    print(C_Y_f)
    print(C_Y_f.str_with_type())
    C_X_fg = H_fg.data(X)
    print(C_X_fg)
    print(C_X_fg.data(id_X.op))


if __name__ == '__main__':
    # test_walking_arrow()
    test_nontriv_comp()
