class RelChange:
    def __init__(self, name, node_a, edge, node_b, add_or_remove):
        self.name = name
        self.node_a = node_a
        self.edge = edge
        self.node_b = node_b
        self.add_or_remove = add_or_remove