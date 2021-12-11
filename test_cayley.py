from category import *
from functor import *
from cayley import *

Z2 = build_Z2()
SC = SetCat()

CayleyF = build_cayley_functor(Z2, SC)

X = Z2.find('X')
zero = Z2.find('0')
one = Z2.find('1')

X_S = CayleyF(X)
zero_S = CayleyF(zero)
one_S = CayleyF(one)

print(f'{zero >> one=}')
print(f'{one >> one=}')

print(f'{(zero_S >> one_S)=}')
print(f'{(one_S >> one_S)=}')
