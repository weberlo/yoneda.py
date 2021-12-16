SUBSCRIPTS = '₀₁₂₃₄₅₆₇₈₉'
def gen_subscript(n: int) -> str:
    if n < 10:
        return SUBSCRIPTS[n]
    else:
        return gen_subscript(n // 10) + SUBSCRIPTS[n % 10]


SYMBOL_REGISTRY: set[str] = set()
class Symbol:
    name: str

    def __init__(self, name: str, assert_unique: bool = False):
        if assert_unique:
            assert name not in SYMBOL_REGISTRY, f"symbol '{name} already used"
        else:
            if name in SYMBOL_REGISTRY:
                # Generate subscripted name
                new_name = name
                i = 1
                while (new_name := name + gen_subscript(i)) in SYMBOL_REGISTRY:
                    i += 1
                name = new_name
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
