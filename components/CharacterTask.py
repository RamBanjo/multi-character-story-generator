#Goal States: So that we can determine whether or not a task is already completed for a character before they have a chance to. If this is true before the character acts out the task, the task is skipped.
#Avoidance States: So that we can determine whether or not a task is impossible for a character before have a chance to complete it. If this is true before the character acts out the task, the task is failed and can no longer be continued.

class CharacterTask:


    '''
    task_name: The name of the task.
    task_action: The list containing actions that the character takes in order to complete the task.
    task_location_name: The name of the location where the task can be performed.
    task_requirement: The list of requirements to perform this task.
    task_giver_name: The name of the actor who assigned this task.
    actor_placeholder_string_list: The list of placeholder strings used in requirements and actions.
    '''
    def __init__(self, task_name: str, task_actions: list, task_location_name:str = None, task_requirement:list = [], task_giver_name:str = None, task_owner_name:str = None, actor_placeholder_string_list:list = [], completion_step = -1, goal_state=[], avoidance_state = []) -> None:
        self.task_name = task_name
        self.task_actions = task_actions
        self.task_location_name = task_location_name
        self.task_complete_status = False
        self.task_giver_name = task_giver_name
        self.task_owner_name = task_owner_name
        self.task_requirement = task_requirement
        self.actor_placeholder_string_list = actor_placeholder_string_list
        self.completion_step = completion_step
        self.goal_state = goal_state
        self.avoidance_state = avoidance_state
        self.placeholder_info_dict = dict()

    # Task Stack?
    # Since certain tasks may take place in more than one location, we will include multiple tasks within one task stack with different locations
    # Once a task in the stack is completed, the task moves on to the next.
    # Entire task stack is marked as complete once all tasks is complete.

#TODO (Testing): Test TaskStack functions
class TaskStack:

    '''
    task_stack: The list of tasks to be performed. A task stack can have as little as 1 task.
    current_task: The index of the current task. If set as -1, this means the entire stack is complete.
    add_step: The absolute step in which the TaskStack is added to a character. None of the tasks performed here may be performed chronologically before the task stack was added.
    '''
    def __init__(self, stack_name:str, task_stack:list = [], task_stack_requirement:list = [], stack_giver_name=None, stack_owner_name=None):
        self.stack_name = stack_name
        self.task_stack = task_stack
        self.current_task_index = 0
        self.actor_placeholder_string_list = []
        self.task_stack_requirement = task_stack_requirement
        self.placeholder_info_dict = dict()
        self.stack_giver_name = stack_giver_name
        self.stack_owner_name = stack_owner_name
        self.remove_from_pool = False
        
    def get_current_task(self):

        if self.current_task_index == -1:
            return None
        
        return self.task_stack[self.current_task_index]
    
    def mark_current_task_as_complete(self, completion_step = 0):
        current_task = self.get_current_task()

        current_task.task_complete_status = True
        current_task.completion_step = completion_step
        self.current_task_index += 1

        if self.current_task_index >= len(self.task_stack):
            self.current_task_index = -1
            self.remove_from_pool = True

    def make_placeholder_string_list(self):

        self.actor_placeholder_string_list.clear()

        for task in self.task_stack:
            self.actor_placeholder_string_list.extend(task.actor_placeholder_string_list)