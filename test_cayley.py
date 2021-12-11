from category import *
from functor import *
from cayley import *


def test_Z5():
    Z5 = build_Zn(5)
    SC = SetCat()

    CayleyF = build_cayley_functor(Z5, SC)

    X = Z5.find('X')
    zero = Z5.find('0')
    one = Z5.find('1')
    two = Z5.find('2')
    three = Z5.find('3')

    X_S = CayleyF(X)
    zero_S = CayleyF(zero)
    one_S = CayleyF(one)
    two_S = CayleyF(two)
    three_S = CayleyF(three)

    print(f'{(zero >> one)=}')
    print(f'{(one >> one)=}')
    print(f'{(three >> three)=}')

    print(f'{(zero_S >> one_S)=}')
    print(f'{(one_S >> one_S)=}')
    print(f'{(three_S >> three_S)=}')


def test_D3():
    D3 = build_D3()
    SC = SetCat()

    CayleyF = build_cayley_functor(D3, SC)

    r0 = D3.find('r0')
    r1 = D3.find('r1')
    f1 = D3.find('f1')
    f2 = D3.find('f2')

    r0_S = CayleyF(r0)
    r1_S = CayleyF(r1)
    f1_S = CayleyF(f1)
    f2_S = CayleyF(f2)

    print(f'{()=}')
    print(f'{(r0 >> r0)=}')
    print(f'{(r0 >> r1)=}')
    print(f'{(r1 >> f1)=}')
    print(f'{(r1 >> f2)=}')

    print(f'{(r0_S >> r0_S)=}')
    print(f'{(r0_S >> r1_S)=}')
    print(f'{(r1_S >> f1_S)=}')
    print(f'{(r1_S >> f2_S)=}')


if __name__ == '__main__':
    test_D3()
