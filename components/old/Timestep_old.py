'''
Timestep!

One timestep refers to one time unit where one story part happens.

Each story part in the timestep happens in a location.
'''

class TimeStep:
    def __init__(self, name, current_world_state):
        self.name = name
        self.story_parts = []
        self.current_world_state = current_world_state
        self.next_timestep = None
        self.previous_timestep = None

    def is_subgraph(self, other_timestep):
        #This Timestep is the subgraph of another timestep when:
        #All story parts of this timestep is contained in the other timestep

        #We also need to test the world state for the other timestep too to make sure that
        #The worldstate is a subset, too

        result = True

        for sp in self.story_parts:
            result = result and (sp in other_timestep.story_parts)

        result = result and self.current_world_state.is_subgraph(other_timestep.current_world_state)

        return result