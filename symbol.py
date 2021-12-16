SYMBOL_REGISTRY: set[str] = set()
class Symbol:
    name: str

    def __init__(self, name: str):
        assert name not in SYMBOL_REGISTRY, f"symbol '{name} already used"
        SYMBOL_REGISTRY.add(name)
        self.name = name

    def __del__(self):
        SYMBOL_REGISTRY.remove(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
