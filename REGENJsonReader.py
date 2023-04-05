#Here is where I would put the ReGEN World State and Rules, if I had any
#I should have done this instead of fucking around with the JSONReader (The rules reader could have waited until later!!!)

from JSONReader import *

regen_story_nodes = read_list_of_objects_from_json(json_file_name="json/ReGEN_Examples/REGENObjects.json", verbose=True)
regen_ws = make_world_state_from_extracted_list_of_objects("Regen WS", regen_story_nodes)
make_connection_from_json(json_file_name="json/ReGEN_Examples/ReGEN_Relations.json", verbose=True, world_state=regen_ws)

#Make Story Parts