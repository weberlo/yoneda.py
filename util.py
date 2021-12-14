CHECK_LAWS = False

SYMBOL_REGISTRY = set()
def gen_symbol(sym):
    assert sym not in SYMBOL_REGISTRY, f'symbol {sym} already used'
    SYMBOL_REGISTRY.add(sym)
    return sym
