list_1 = [True, False, False, False, False]
list_2 = [False, False, False, False, False]
list_3 = [False, False, False, False, False]
list_4 = [False, False, False, False, False]
list_5 = [False, False, False, False, False]


def get_metric_score(graph:list):
    return (graph.count(True) / len(graph)) * 100

def get_multigraph_metric_score(current_graph : list, previous_graphs = None, score_retention:float = 0):
    
    current_score = get_metric_score(current_graph)

    if score_retention > 1:
        score_retention = 1
    if score_retention < 0:
        score_retention = 0
    
    if previous_graphs != None and score_retention > 0:
        past_scores = [get_metric_score(past_graph) for past_graph in previous_graphs]
        forgotten_past_score = []
        # past_graph_total_nodes = []
        # forgotten_past_graph_total_nodes = []

        for past_graph in previous_graphs:
            past_scores.append(get_metric_score(past_graph))
            # this_graphlength = past_graph.get_longest_path_length_by_character(character)
            # past_score_times_len.append(this_graphscore * this_graphlength)
            # past_graph_total_nodes.append(this_graphlength)

        
        final_divider = 1.0

        for index in range(0, len(previous_graphs)):
            
            forgetfulness_exponent = (len(previous_graphs) - index)
            forgetfulness_multiplier = score_retention ** forgetfulness_exponent
            forgotten_past_score.append(past_scores[index] * forgetfulness_multiplier)
            final_divider += forgetfulness_multiplier

            # forgotten_past_score_times_len.append(past_score_times_len[index] * forgetfulness_multiplier)
            # forgotten_past_graph_total_nodes.append(past_graph_total_nodes[index] * forgetfulness_multiplier)
            # forgetfulness_exponent -= 1

        # current_graphlength = self.get_longest_path_length_by_character(character=character)
        # current_score_multed = current_score * current_graphlength
        forgotten_past_score.append(current_score)
        current_score = sum(forgotten_past_score) / final_divider

    return current_score

print(get_multigraph_metric_score(current_graph = list_1, previous_graphs = [list_2, list_3, list_4, list_5]))
