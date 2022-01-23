class Group:
    # elts : Set[Any]
    # e : elts
    # table : elts -> elts -> elts

    def __init__(self, elts, e, table):
        self.elts = elts
        self.e = e
        self.table = table


class GroupElt:
    def __init__(self, elt, group):
        self.elt = elt
        self.group = group

    def __rshift__(self, other):
        g = self.group
        assert g == other.group
        return GroupElt(g.table[(self.elt, other.elt)], g)

    def __str__(self):
        return str(self.elt)


Z2 = Group({'0', '1'}, '0', {
    ('0', '0'): '0',
    ('0', '1'): '1',
    ('1', '0'): '1',
    ('1', '1'): '0',
})
zero = GroupElt('0', Z2)
one = GroupElt('1', Z2)

print(zero >> one >> zero >> one >> one)
