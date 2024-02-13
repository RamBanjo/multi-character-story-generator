import sys

sys.path.insert(0,'')

from components.StoryMetrics import *
from components.StoryObjects import *
from components.WorldState import *
from components.StoryGraphTwoWS import *

#Here is how we will want to test our Metrics Functions:

# Testing measuring costs
# Scenario 1: Test Cost of a Story: See if it can count Costly Nodes properly
# Scenario 2: Test Uniqueness of a Story: See if it can count unique nodes properly
# Scenario 3: Test Jointability of a Story: See if it can count Joint Nodes properly
# Scenario 4: Test Preference of a Story: See if it can count Important Nodes properly

# Testing score calculations
# Scenario 1: Test Cost Score Calculation: See if it can get the score of Cost properly
# Scenario 2: Test Uniqueness Score Calculation: See if it can get the score of Uniqueness properly
# Scenario 3: Test Jointability Score Calculation: See if it can get the score of Jointability properly
# Scenario 4: Test Preference Score Calculation: See if it can get the score of Preference properly

# Testing "Follows Metric Rules" functions
# Scenario 1: Test Cost Metric Rule Follow (True and False)
# Scenario 2: Test Uniqueness Metric Rule Follow (True and False)
# Scenario 3: Test Jointability Metric Rule Follow (True and False)
# Scenario 4: Test Preference Metric Rule Follow (True and False)
