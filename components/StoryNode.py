from numpy import character


class StoryNode:
    def __init__(self, name, biases, biasweight, tags, charcount, timestep = 0):
        
        #the name of this action.
        self.name = name
        
        #biases. forbids characters outside of this range from performing this action.
        self.biases = biases

        #bias weight. How much this action will affect the bias of the character performing it.
        self.biasweight = biasweight
        
        #tags for searching actions of a specific type.
        #If it's an end node, it will be among the tags.
        self.tags = tags
        
        #charcount will be 1 if it's single char node, if it's joint then it will be more than 1
        self.charcount = charcount
        
        #set of characters acting. if it's a template, then it should be blank
        self.actor = []
        
        #set of targets of this action. if it's a template, then it should be blank.
        self.target = []

        #the location where this story happens. If it's a template, then it should be None.
        self.location = None
        
        #dict of nodes that leads to this node. Each entry has character's unique ID as key and points to
        #the node that character performed before arriving at this node.
        self.previous_nodes = dict()
        
        #dict of nodes that continue from here. Each entry has character's unique ID as key and points to
        #the node that character will perform after leaving this node.
        self.next_nodes = dict()

        #timestep property. For template storynodes it will be 0. But once it is assigned to the story the number will never change.
        #This will prevent stories from different timestep from being blended together.
        
        #TODO: An object that defines the change in relationship for characters and objects in this story node

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        self.location = new_location

    def add_actor(self, new_actor):
        self.actor.append(new_actor)

    def remove_actor(self, remove_actor):
        self.actor.remove(remove_actor)

    def add_target(self, new_target):
        self.target.append(new_target)
    
    def remove_target(self, remove_target):
        self.target.remove(remove_target)

    def get_actor_names(self):
        actornamestring = ""
        for actorobject in self.actor:

            if actorobject is not None:
                actornamestring += actorobject.get_name()
            else:
                actornamestring += "None"
                

            actornamestring += ", "
        return actornamestring[:-2]


    def __str__(self) -> str:
        return self.get_name() + ": " + self.get_actor_names()

    def __eq__(self, rhs):
        return self.get_name() == rhs.get_name() and sorted(self.actor) == sorted(rhs.actor) and sorted(self.target) == sorted(rhs.target)

    def __ge__(self, rhs):
        return self.get_name() >= rhs.get_name()
    '''
    This function adds next_node as the next node for the character object character_reference

    It will also add self as one of next_node's previous nodes! Convenient!
    '''
    def add_next_node(self, next_node, character_reference):

        char_name = None

        if character_reference is not None:
            char_name = character_reference.get_name()

        self.next_nodes[char_name] = next_node
        next_node.previous_nodes[char_name] = self
        #next_node.add_actor(character_reference)


    '''
    First, it removes itself from next_node's previous nodes

    Then, it removes next_node from its own next nodes
    '''
    def remove_next_node(self, character_reference):

        char_name = None

        if character_reference is not None:
            char_name = character_reference.get_name()

        next_node = self.next_nodes[char_name]

        del next_node.previous_nodes[char_name]
        del self.next_nodes[char_name]


