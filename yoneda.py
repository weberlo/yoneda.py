import category

def H_obj(X: 'Object[C]'):
    C_op = X.cat.opposite()
    X_op = C_op.find_obj(X)
    return HomFunctor(None, X_op)

def H_mor(f: 'Morphism[C]'):
    C_op = f.cat.opposite()
    pass
