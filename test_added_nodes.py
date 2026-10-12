import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_added_nodes(graph1, graph2):
    # Extract node IDs from the first graph
    node_ids_graph1 = {node['id'] for node in graph1.get('nodes', [])}

    # Find nodes in the second graph that are not in the first graph
    added_nodes = [node for node in graph2.get('nodes', []) if node['id'] not in node_ids_graph1]

    return added_nodes

def modify_and_save_graph(file1, file2, output_file):
    graph1 = load_json(file1)
    graph2 = load_json(file2)

    # Find added nodes
    added_nodes = find_added_nodes(graph1, graph2)

    # Get IDs of added nodes for easy lookup
    added_node_ids = {node['id'] for node in added_nodes}

    # Modify the color of added nodes in graph2
    for node in graph2.get('nodes', []):
        if node['id'] in added_node_ids:
            node['attributes']['color'] = [0, 255, 0]  # Change color to green (RGB)

    # Save the modified graph2 to a new JSON file
    with open(output_file, 'w') as file:
        json.dump(graph2, file)

# File paths for the input and output files
input_file1 = 'dsg_obj_backend_run2.json'  # Replace with actual file path
input_file2 = 'dsg_obj_backend_run1.json'  # Replace with actual file path
output_file = 'object_backend_run2_1.json'  # Replace with actual file path

# Run the function with the specified file paths
if __name__ == '__main__':
    modify_and_save_graph(input_file1, input_file2, output_file)
