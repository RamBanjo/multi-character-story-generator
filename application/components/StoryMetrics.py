from enum import Enum

class MetricType(Enum):
    COST = 0
    UNIQUE = 1
    JOINTS = 2
    PREFER = 3

class MetricMode(Enum):
    LOWER = 0
    STABLE = 1
    HIGHER = 2

class StoryMetric:
    def __init__(self, metric_type:MetricType, value:int, metric_mode:MetricMode, character_object):
        
        self.metric_type = metric_type
        self.value = value
        self.metric_mode = metric_mode
        self.character_object = character_object

    def __str__(self) -> str:
        return self.metric_type.name + " " + self.metric_mode.name + " " + str(self.value) + " for " + self.character_object.get_name()
