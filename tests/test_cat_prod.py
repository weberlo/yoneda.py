from category import *
from instances.category import *
from instances.category.set_cat import *
from instances.category.product import prod

def test_Z2_times_Z2():
    Z2 = build_Zn(2)

    Z2_x_Z2 = prod(Z2, Z2)
    assert len(Z2_x_Z2.objs) == 1, 'a product of groups should still have only one object'
    X_x_X = next(iter(Z2_x_Z2.objs))
    zero = Z2.find_mor_by_name('0')
    one = Z2.find_mor_by_name('1')
    def get_prod_mor(f1, f2):
        return Z2_x_Z2.find_mor_by_data(X_x_X, (f1.data, f2.data), X_x_X)

    zero_x_zero = get_prod_mor(zero, zero)
    assert zero_x_zero >> zero_x_zero == zero_x_zero, 'identity of product category must be product of constituent identities'
    zero_x_one = get_prod_mor(zero, one)
    assert zero_x_zero >> zero_x_one == zero_x_one
    one_x_zero = get_prod_mor(one, zero)
    assert zero_x_zero >> one_x_zero == one_x_zero
    one_x_one = get_prod_mor(one, one)
    assert zero_x_one >> one_x_zero == one_x_one
    assert zero_x_one >> one_x_zero != one_x_zero
    assert one_x_one >> one_x_one == zero_x_zero


if __name__ == '__main__':
    test_Z2_times_Z2()
