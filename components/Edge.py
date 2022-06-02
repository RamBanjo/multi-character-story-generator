class Edge:
    def __init__(self, name, from_node=None, to_node=None, value=0):
        
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        
        #value exists in the case of character to character relationships
        self.value = value
        
    def __str__(self):
        return self.name + " (" + self.from_node.name + " ---> " + self.to_node.name + ")"

    def __eq__(self, rhs):
        return self.name == rhs.name and self.from_node == rhs.from_node and self.to_node == rhs.to_node

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name