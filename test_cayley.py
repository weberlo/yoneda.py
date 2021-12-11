from category import *
from functor import *
from cayley import *

Z2 = build_Zn(5)
SC = SetCat()

CayleyF = build_cayley_functor(Z2, SC)

X = Z2.find('X')
zero = Z2.find('0')
one = Z2.find('1')
two = Z2.find('2')
three = Z2.find('3')

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
