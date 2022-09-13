class ObjectNode:
    def __init__(self, name, tags={"Type": "Object"}):
        
        #What this object will be referred to as. Assumed to be unique.
        self.name = name
        
        #Tags of this object, as a dict. Mutable.
        self.tags = tags
        
        #The list of relationships this object has towards other objects.
        self.outgoing_edges = []
        
        #The list of relationships that point to this object.
        self.incoming_edges = []

    def set_tag(self, attribute, new_value):
        self.tags[attribute] = new_value

    def remove_tag(self, attribute):
        del self.tags[attribute]

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name
        
    def get_incoming_edge(self, edgename):
        return_edge = []
        for edge in self.incoming_edges:
            if edge.name == edgename:
                return_edge += [edge]
        return return_edge
    
    def get_outgoing_edge(self, edgename):
        return_edge = []
        for edge in self.outgoing_edges:
            if edge.name == edgename:
                return_edge += edge
        return return_edge

    def add_incoming_edge(self, edge):
        edge.to_node = self
        self.incoming_edges.append(edge)
    
    def add_outgoing_edge(self, edge):
        edge.from_node = self
        self.outgoing_edges.append(edge)

    def remove_incoming_edge(self, edge):
        edge.to_node = None
        self.incoming_edges.remove(edge)

    def remove_outgoing_edge(self, edge):
        edge.from_node = None
        self.outgoing_edges.remove(edge)

    def __str__(self) -> str:
        return self.get_name()

    def __eq__(self, rhs) -> bool:
        return self.name == rhs.name

    def __ge__(self, rhs):
        return self.get_name() >= rhs.get_name()


class CharacterNode(ObjectNode):

    DEFAULT_BIASES = {"lawbias": 0, "moralbias": 0}

    def __init__(self, name, biases=DEFAULT_BIASES, tags={"Type": "Character"}, start_timestep=0):

        #call super constructor
        super().__init__(name, tags)

        #The bias values of this character as a dict. Mutable.
        #Only exists if it's a character.
        #Set to None if it's not.
        self.biases = biases

        #The first timestep that this character should appear in.
        #If it's not a character, set to 0.
        self.start_timestep = start_timestep

class LocationNode(ObjectNode):
    def __init__(self, name, tags={"Type": "Location"}):
        super().__init__(name, tags)

    def get_adjacent_locations_list(self):
        adjacencies = self.get_incoming_edge("adjacent_to")
        return adjacencies
        
#alice = StoryCharacter("Alice", {'lawbias': 0, 'moralbias': 0}, {"Race":"Human", "Job":"Spellcaster", "Life":"Alive", "Gender":"Female"}, 5)

#print(alice.name)
#print(alice.biases)
#print(alice.tags)
#print(alice.start_timestep)