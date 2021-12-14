from hom_functor import *
from cat_insts import *
from yoneda import *

WA = build_walking_arrow()
one = WA.find('1')
two = WA.find('2')
f = WA.find('f')
id_1 = WA.find('id_1')
id_2 = WA.find('id_2')

PshC = PresheafCat()
H = build_yoneda_embed(WA, PshC)

print(H(one))
print(H(two))
print(H(f))
print(H(id_1))
print(H(id_2))
