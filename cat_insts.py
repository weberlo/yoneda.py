from category import *

def build_Zn(n: int):
    Zn = Category()

    [X] = Zn.add_objs(['X'])

    mors = [Morphism(X, str(i), X) for i in range(n)]
    # 0 is the identity
    mors[0].is_ident = True
    mors = Zn.add_mors(mors)

    comp_dict = {}
    for a in mors:
        for b in mors:
            comp_dict[(a, b)] = mors[(int(a.sym) + int(b.sym)) % n]
    def comp_rule(f: Morphism, g: Morphism):
        return comp_dict[(f, g)]
    Zn.add_comp_rule(comp_rule)

    return Zn


def cayley_table_to_comp_dict(order, table):
    comp_dict = {}
    for i, a in enumerate(order):
        for j, b in enumerate(order):
            # Row `m` and column `n` of the table correspond to `order[m] *
            # order[n]`, as this is the Cayley table convention.  However,
            # recall this is in *classical* composition order,but we want the
            # entry `(a, b)` to correspond to the forward composition `a >> b`,
            # so we grab `table[j][i]`, rather than `table[i][j]`.
            comp_dict[(a, b)] = table[j][i]
    return comp_dict


# TODO generalize to Dn
def build_D3():
    n = 3
    D3 = Category()

    [X] = D3.add_objs(['X'])

    # Rotations
    mors = [Morphism(X, f'r{i}', X) for i in range(n)]
    # Reflections
    mors += [Morphism(X, f'f{i}', X) for i in range(n)]
    # r0 is the identity
    mors[0].is_ident = True

    [r0, r1, r2, f0, f1, f2] = D3.add_mors(mors)

    comp_dict = cayley_table_to_comp_dict(
        order=[r0, r1, r2, f0, f1, f2],
        table=[
            [r0, r1, r2, f0, f1, f2],  # r0
            [r1, r2, r0, f1, f2, f0],  # r1
            [r2, r0, r1, f2, f0, f1],  # r2
            [f0, f2, f1, r0, r2, r1],  # f0
            [f1, f0, f2, r1, r0, r2],  # f1
            [f2, f1, f0, r2, r1, r0],  # f2
        ]
    )
    def comp_rule(f: Morphism, g: Morphism):
        return comp_dict[(f, g)]
    D3.add_comp_rule(comp_rule)

    return D3


def build_walking_arrow():
    Two = Category()

    [one, two] = Two.add_objs(['1', '2'])

    mors = [
        Morphism(one, 'id_1', one, is_ident=True),
        Morphism(one, 'f', two),
        Morphism(two, 'id_2', two, is_ident=True)
    ]
    [id_1, f, id_2] = Two.add_mors(mors)

    comp_dict = {
        (id_1, id_1): id_1,
        (id_1, f): f,
        (f, id_2): f,
        (id_2, id_2): id_2,
    }
    def comp_rule(f: Morphism, g: Morphism):
        return comp_dict[(f, g)]
    Two.add_comp_rule(comp_rule)

    return Two
