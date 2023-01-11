from components.RewriteRuleWithWorldState import *

#Test Scenario:
#Alice goes to Bar
#Bob goes to Bar
#The rule says that if both characters are going to Bar, they can Talk with each other
#For two characters to talk, they must be in the same location
#We probably don't need to test Check Add Joint Validity that much considering we cobbled up functions that we know works together
#However, we might need to test the insert split function because that's a new thing we did