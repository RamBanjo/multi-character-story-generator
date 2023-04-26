
class CharacterTask:


    '''
    task_name: The name of the task.
    task_action: The list containing actions that the character takes in order to complete the task.
    task_location_name: The name of the location where the task can be performed.
    task_requirement: The list of requirements to perform this task.
    task_giver_name: The name of the actor who assigned this task.
    actor_placeholder_string_list: The list of placeholder strings used in requirements and actions.
    '''
    def __init__(self, task_name: str, task_actions: list, task_location_name:str = None, task_requirement:list = [], task_giver_name:str = None, actor_placeholder_string_list:list = []) -> None:
        self.task_name = task_name
        self.task_actions = task_actions
        self.task_location_name = task_location_name
        self.task_complete_status = False
        self.task_giver_name = task_giver_name
        self.task_requirement = task_requirement
        self.actor_placeholder_string_list = actor_placeholder_string_list

    #TODO: Task Stack?
    # Since certain tasks may take place in more than one location, we will include multiple tasks within one task stack with different locations
    # Once a task in the stack is completed, the task moves on to the next.
    # Entire task stack is marked as complete once all tasks is complete.

class TaskStack:

    '''
    task_stack: The list of tasks to be performed. A task stack can have as little as 1 task.
    current_task: The index of the current task. If set as -1, this means the entire stack is complete.
    '''
    def __init__(self, stack_name:str, task_stack:list = [], current_task:int = 0):
        self.stack_name = stack_name
        self.task_stack = task_stack
        self.current_task = current_task
        
    def get_current_task(self):
        return self.task_stack[self.current_task]
    
    def mark_current_task_as_complete(self):
        self.get_current_task().task_complete_status = True
        self.current_task += 1

        if self.current_task >= len(self.task_stack):
            self.get_current_task = -1