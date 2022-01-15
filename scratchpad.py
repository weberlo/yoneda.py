# In this file, we model (extensionally!) the finite group with the Cayley table below:
#    | e | a
#  ==========
#  e | e | a
#  ----------
#  a | a | e
e = lambda x: x
elts = [e]

def a(x):
    if x == e:
        return a
    elif x == a:
        return e
    elif eq(x, e, elts):
        print('here')
        return a
    elif eq(x, a, elts):
        print('heree')
        return e
    assert False


# We close the loop here!
elts.append(a)

#
# Group definition end
#

graph_to_elt = {}


def comp_rule(f, g, elts):
    res = lambda x: g(f(x))
    res_graph = graph(res, elts)
    if res_graph not in graph_to_elt:
        graph_to_elt[res_graph] = res
    return res


# def find_base(x, S):
#     if x in S:
#         return x
#     return find_base(graph_to_elt[graph(x, S)], S)


def graph(x, S):
    return frozenset([(y, x(y)) for y in S])


def eq(x, y, S):
    return graph(x, S) == graph(y, S)


# # Add all of the base elements to the graph-to-element cache.
# for elt in elts:
#     graph_to_elt[graph(elt, elts)] = elt


aa = comp_rule(a, a, elts)
aaaa = comp_rule(aa, aa, elts)
ea = comp_rule(e, a, elts)

print(f'{elts=}')
print(f'{graph(e, elts)=}')
print(f'{graph(a, elts)=}')
print(f'{graph(aa, elts)=}')
print(f'{eq(e, aa, elts)=}')
print(f'{eq(aa, aaaa, elts)=}')
print(f'{eq(e, aaaa, elts)=}')
print(f'{eq(ea, a, elts)=}')
print(f'{eq(ea, e(a), elts)=}')
print(f'{eq(a, a(e), elts)=}')
print(f'{eq(a, a(aa), elts)=}')
print(f'{eq(e, aa(aa), elts)=}')
