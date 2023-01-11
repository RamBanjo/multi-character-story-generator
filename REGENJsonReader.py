from JSONReader import *

regen_story_nodes = read_list_of_objects_from_json(json_file_name="json/ReGEN_Examples/REGENObjects.json", verbose=True)
regen_ws = make_world_state_from_extracted_list_of_objects("Regen WS", regen_story_nodes)
make_connection_from_json(json_file_name="json/ReGEN_Examples/ReGEN_Relations.json", verbose=True, world_state=regen_ws)

#Make Story Parts