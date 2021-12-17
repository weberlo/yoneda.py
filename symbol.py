SUBSCRIPTS = '₀₁₂₃₄₅₆₇₈₉'
def gen_subscript(n: int) -> str:
    if n < 10:
        return SUBSCRIPTS[n]
    else:
        return gen_subscript(n // 10) + SUBSCRIPTS[n % 10]


def gen_fresh(base: str) -> str:
    if base not in SYMBOL_REGISTRY:
        return base
    # Generate subscripted name
    res = base
    i = 1
    while (res := base + gen_subscript(i)) in SYMBOL_REGISTRY:
        i += 1
    return res


SYMBOL_REGISTRY: set[str] = set()
class Symbol:
    name: str

    def __init__(self, name: str):
        assert name not in SYMBOL_REGISTRY, f"symbol '{name} already used"
        SYMBOL_REGISTRY.add(name)
        self.name = name

    def __del__(self):
        if hasattr(self, 'name'):
            SYMBOL_REGISTRY.remove(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
