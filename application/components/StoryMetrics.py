from enum import Enum


class StoryMetric:
    def __init__(self, metric_type, value, metric_mode, character_object):
        
        self.metric_type = metric_type
        self.value = value
        self.metric_mode = metric_mode
        self.character_object = character_object

class MetricType(Enum):
    COST = 0
    UNIQUE = 1
    JOINTS = 2
    PREFER = 3

class MetricMode(Enum):
    LOWER = 0
    STABLE = 1
    HIGHER = 2
    