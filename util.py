CHECK_LAWS = False

SYMBOL_REGISTRY = set()
def gen_symbol(sym):
    assert sym not in SYMBOL_REGISTRY, 'symbol already used'
    SYMBOL_REGISTRY.add(sym)
    return sym
