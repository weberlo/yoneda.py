CHECK_LAWS = False

SYMBOL_REGISTRY: set[str] = set()
class Symbol:
    name: str

    def __init__(self, name: str):
        assert name not in SYMBOL_REGISTRY, f"symbol '{name} already used"
        SYMBOL_REGISTRY.add(name)
        self.name = name
