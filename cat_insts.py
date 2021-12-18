from category import *
from util import *

def build_Zn(n: int) -> Category[None, int]:
    X = Object('X', None)

    mors = [Morphism(X, str(i), i, X) for i in range(n)]

    comp_dict: dict[tuple[Morphism[None, int], Morphism[None, int]], Morphism[None, int]] = {}
    for a in mors:
        for b in mors:
            comp_dict[(a, b)] = mors[(a.data + b.data) % n]

    return Category({X}, set(mors), dict_as_comp_rule(comp_dict))


# TODO generalize to Dn
def build_D3() -> Category[None, None]:
    n = 3

    X = Object('X', None)

    # Rotations
    mors = [Morphism(X, f'r{i}', None, X) for i in range(n)]
    # Reflections
    mors += [Morphism(X, f'f{i}', None, X) for i in range(n)]

    [r0, r1, r2, f0, f1, f2] = mors

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
    def comp_rule(f: Morphism[None, None], g: Morphism[None, None]) -> Morphism[None, None]:
        return comp_dict[(f, g)]

    return Category({X}, set(mors), comp_rule)


def build_walking_arrow() -> Category[None, None]:
    [one, two] = [Object('1', None), Object('2', None)]

    [id_1, f, id_2] = [
        Morphism(one, 'id_1', None, one),
        Morphism(one, 'f', None, two),
        Morphism(two, 'id_2', None, two)
    ]

    comp_dict = {
        (id_1, id_1): id_1,
        (id_1, f): f,
        (f, id_2): f,
        (id_2, id_2): id_2,
    }

    return Category({one, two}, {id_1, f, id_2}, dict_as_comp_rule(comp_dict))


# TODO write function to build categories from sketches
def build_nontriv_comp() -> Category[None, None]:
    [X, Y, Z] = [
        Object('X', None),
        Object('Y', None),
        Object('Z', None)
        ]

    [id_X, id_Y, id_Z, f, g, f_g] = [
        Morphism(X, 'id_X', None, X),
        Morphism(Y, 'id_Y', None, Y),
        Morphism(Z, 'id_Z', None, Z),
        Morphism(X, 'f', None, Y),
        Morphism(Y, 'g', None, Z),
        Morphism(X, 'f;g', None, Z),
    ]

    comp_dict = {
        (id_X, id_X): id_X,
        (id_Y, id_Y): id_Y,
        (id_Z, id_Z): id_Z,
        (id_X, f): f,
        (f, id_Y): f,
        (id_Y, g): g,
        (g, id_Z): g,
        (f, g): f_g,
        (id_X, f_g): f_g,
        (f_g, id_Z): f_g,
    }

    return Category(
        {X, Y, Z},
        {id_X, id_Y, id_Z, f, g, f_g},
        dict_as_comp_rule(comp_dict))
