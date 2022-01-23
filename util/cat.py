from category import *
from typing import Callable

def cayley_table_to_comp_dict(
        order: list[Morphism[O, M]],
        table: list[list[Morphism[O, M]]]
        ) -> dict[tuple[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]:
    comp_dict: dict[tuple[Morphism[O, M], Morphism[O, M]], Morphism[O, M]] = {}
    for i, a in enumerate(order):
        for j, b in enumerate(order):
            # Row `m` and column `n` of the table correspond to `order[m] *
            # order[n]`, as this is the Cayley table convention.  However,
            # recall this is in *classical* composition order,but we want the
            # entry `(a, b)` to correspond to the forward composition `a >> b`,
            # so we grab `table[j][i]`, rather than `table[i][j]`.
            comp_dict[(a, b)] = table[j][i]
    return comp_dict


def dict_as_comp_rule(
    comp_dict: dict[tuple[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]
    ) -> Callable[[Morphism[O, M], Morphism[O, M]], Morphism[O, M]]:
    def comp_rule(f: Morphism[O, M], g: Morphism[O, M]) -> Morphism[O, M]:
        return comp_dict[(f, g)]
    return comp_rule
