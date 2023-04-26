from components.CharacterTask import CharacterTask


class ObjectNode:
    def __init__(self, name, tags={"Type": "Object"}, **kwargs):
        
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

    def print_all_tags(self):
        print("==== Tags found on", self.get_name(), "====")
        for key, value in self.tags.items():
            print(key, ":" ,value)

    #This assumes that only one thing (location or character) can hold another item at a time.
    def get_holder(self, holds_rel_name = "holds"):
        holds_edge = self.get_incoming_edge(holds_rel_name)
        return holds_edge[0].from_node

    def get_list_of_things_held_by_this_item(self, holds_rel_name = "holds"):
        things_list = []

        for edge in self.outgoing_edges:
            if edge.get_name() == holds_rel_name:
                things_list.append(edge.to_node)

        return things_list

    def check_if_this_item_holds_item_with_tag(self, tag, value, holds_rel_name = "holds"):
        held_items_list = self.get_list_of_things_held_by_this_item(holds_rel_name)

        for thing in held_items_list:
            if thing.check_if_this_item_has_tag(tag, value):
                return True

        return False

    #If both tag and value are given, both must match.
    #If only tag is given and value is None, then only the tag has to exist.
    def check_if_this_item_has_tag(self, tag, value=None):

        if value == None:
            return tag in self.tags.keys()
        else:
            return (tag, value) in self.tags.items()


    def __str__(self) -> str:
        return self.get_name()

    def __eq__(self, rhs) -> bool:
        return self.name == rhs.name

    def __ge__(self, rhs):
        return self.get_name() >= rhs.get_name()

    def __lt__(self, rhs):
        return self.get_name() < rhs.get_name()


class CharacterNode(ObjectNode):

    DEFAULT_BIASES = {"lawbias": 0, "moralbias": 0}

    def __init__(self, name, biases=DEFAULT_BIASES, tags={"Type": "Character"}, start_timestep=0, **kwargs):

        #call super constructor
        super().__init__(name, tags)

        #The bias values of this character as a dict. Mutable.
        #Only exists if it's a character.
        #Set to None if it's not.
        self.biases = biases

        #The first timestep that this character should appear in.
        #If it's not a character, set to 0.
        self.start_timestep = start_timestep

        #List of Tasks will start off as an empty dict then gradually gets populated after the character receives tasks from certain sources
        self.list_of_task_stacks = []

    def add_task_stack(self, task_stack):
        self.list_of_tasks.append(task_stack)

    def mark_task_status(self, task_name: str, task_status: bool):
        current_task = self.list_of_tasks.get(task_name, None)

        if current_task is not None:
            current_task.task_complete_status = task_status

class LocationNode(ObjectNode):
    def __init__(self, name, tags={"Type": "Location"}, **kwargs):
        super().__init__(name, tags)

    def get_adjacent_locations_list(self, adjacent_rel_name = "adjacent_to"):
        adjacencies = self.get_incoming_edge(adjacent_rel_name)
        return adjacencies

        
#alice = StoryCharacter("Alice", {'lawbias': 0, 'moralbias': 0}, {"Race":"Human", "Job":"Spellcaster", "Life":"Alive", "Gender":"Female"}, 5)

#print(alice.name)
#print(alice.biases)
#print(alice.tags)
#print(alice.start_timestep)

