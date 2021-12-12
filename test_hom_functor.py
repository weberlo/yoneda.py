from hom_functor import *
from cat_insts import *


Two = build_walking_arrow()
one = Two.find('1')
two = Two.find('2')
f = Two.find('f')
id_1 = Two.find('id_1')
id_2 = Two.find('id_2')

SC = SetCat()

Two_1 = build_covariant_hom_functor(Two, one, SC)
print(Two_1(one))
print(Two_1(two))
print(Two_1(f))
print(Two_1(id_1))
print(Two_1(id_2))
