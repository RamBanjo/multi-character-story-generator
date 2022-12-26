from components.StoryObjects import *

node_data = {"tags":{"Type":"Placeholder","Value":"Worthless"}}
test_node = ObjectNode(name = "Something", **node_data)

print(test_node)
print(test_node.tags)