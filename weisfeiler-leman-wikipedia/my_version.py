"""
File implements the 1 dimension Weisfeiler-Leman algorithm, as described
(but cleand up) at:

https://en.wikipedia.org/w/index.php?title=Weisfeiler_Leman_graph_isomorphism_test&oldid=1268456079
"""

#########
#
#  Inputs
#
#########

g5_00 = {0: [1, 2, 4], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [0, 3]}
g5_01 = {0: [3, 4], 1: [2, 3, 4], 2: [1, 3], 3: [0, 1, 2], 4: [0, 1]}
g5_02 = {0: [1, 2, 4], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [0, 3]}


__DEBUG__ = False



def combine_graphs(g1, g2):
    """Combines two graphs, g1 and g2, returns a single disjoin graph"""
    g = g1.copy()
    start_key_value = max(g.keys()) + 1
    for key, values in g2.items():
        new_key = start_key_value + key
        g[new_key] = []
        for v in values:
            g[new_key].append(v+start_key_value)

    return g


def weisfeiler_leman(g0, g1):
    """Executes the Weisfeiler-Leman algoright on graphs g1 and g2
        returns a tuple of the certificates (hashes of colors)
    """
    g = combine_graphs(g0, g1)
    color_to_label_map = {}
    node_labels = {i:0 for i in g}  # Set each nodes glabel???  to zero

    node_labels__unique_count = 1
    next_label = 1  # value of the next label to assign

    done = False
    while not done:
        new_node_labels = {}
        new_node_labels__unique_count = 0
        for node, neighbors in g.items():
            my_label = str(node_labels[node]) # fetch our label
            neighbor_labels = sorted([str(node_labels[neighbor]) for neighbor in neighbors]) # create a sorted list of labels of this neighbor, as strings
            color = f'{my_label}_{"_".join(neighbor_labels)}' # append labels of all neighbors to our label, this is our color

            # if color is not in the current color_to_label_map...
            if  color not in color_to_label_map:
                color_to_label_map[color] = next_label  # add it, using the next available label
                next_label += 1 # increment the next available label
                new_node_labels__unique_count += 1  # increment the unique label count

            new_node_labels[node] = color_to_label_map[color] # Fetch the label representing our color, and set our label to that value

            if __DEBUG__:
                print(f'Node: {node}  current round label: {my_label}  color: {color}  next round label: {new_node_labels[node]}')

        # if no new labels were created this round, then the colors have stabilized
        if node_labels__unique_count == new_node_labels__unique_count:
            done = True  # we are done, and can exit the loop
        else:
            # Otherwise, new labels were found, the colors have not yet stabilized
            #   Set the node_labels and unique counts equal to the new versions, ready for next round
            node_labels__unique_count = new_node_labels__unique_count
            node_labels = new_node_labels.copy()

        if __DEBUG__:
            print('\n')


    #split the joined graph node labels to represent the original graph

    g0_length = len(g0)
    g0_final_node_labels = sorted([node_labels[x] for x in sorted(node_labels.keys())[:g0_length]])  # Get the keys that are in g0 and fetch the node_labels for each of those nodes, then sort
    g1_final_node_labels = sorted([node_labels[x] for x in sorted(node_labels.keys())[g0_length:]])  # Get the keys that are in g1 and fetch the node_labels for each of those nodes, then sort

    g0_certificate = '_'.join(map(str,g0_final_node_labels))  # create certificate, or "hash" of the g0 graph nodes
    g1_certificate = '_'.join(map(str,g1_final_node_labels))  # create certificate, or "hash" of the g1 graph nodes


    # certificate1 = '_'.join(map(str,sorted(list(node_labels.values())[len(g0):])))  # create certificate, or "hash" of the graph
    return g0_certificate, g1_certificate



for a, b in ((g5_00, g5_01), (g5_00, g5_02), (g5_01, g5_02)):
    cert0, cert1 = weisfeiler_leman(a, b)
    print(cert0)
    print(cert1)
