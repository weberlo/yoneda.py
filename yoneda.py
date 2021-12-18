from category import *
from functor import *
from hom_functor import *
from nat_trans import *
from presheave import *

# TODO maybe there should be a singleton Set instance
# SC = SetCat()

def build_yoneda_embed(
        C: Category[CO, CM],
        PshC: PshCat[CO, CM]
        ) -> Functor[CO, CM, Psh[CO, CM], PshNatTrans[CO, CM]]:
    SC = PshC.set_cat

    def obj_map(X: Object[CO]) -> PshObj[CO, CM]:
        F = build_contravariant_hom_functor(C, X, SC)
        return PshC.find_obj_by_functor(F, name=f'{C}(-,{X})')

    def mor_map(f: Morphism[CO, CM]) -> PshMor[CO, CM]:
        X = f.src
        Y = f.tgt
        C_·_X_obj = obj_map(X)
        C_·_Y_obj = obj_map(Y)
        C_·_X = C_·_X_obj.data
        C_·_Y = C_·_Y_obj.data
        def eta(A: Object[CO]) -> SetMor:
            C_A_X = C_·_X.obj_map(A)
            C_A_Y = C_·_Y.obj_map(A)
            data: Callable[[Morphism[CO, CM]], Morphism[CO, CM]] = lambda x: x >> f
            # We need a unique name for each morphism, even though they're all
            # formed by postcomposition with `f`.
            # name = f'(· ∈ {C_A_X}) >> {f}'
            name = f'{C}({A}, {f})'
            # name = f'· >> {f}'
            return SC.find_mor_by_fn(C_A_X, data, C_A_Y, name)
        nat_trans = NatTrans[CO, CM, set[Any], Fn](C_·_X, C_·_Y, eta)
        # name = f'∀ A: Ob({C}). {C}(A, {f})'
        name = f'{C}(-,{f})'
        return PshC.find_mor_by_nat_trans(C_·_X_obj, nat_trans, C_·_Y_obj, name)

    return Functor(C, PshC, obj_map, mor_map, Variance.Covariant)
