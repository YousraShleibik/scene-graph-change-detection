'''import json

# Function to load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to find new nodes and extract their ID and name
def find_and_extract_new_nodes(old_data, new_data):
    old_node_ids = {node['id'] for node in old_data['nodes']}
    new_node_info = []
    for node in new_data['nodes']:
        if node['id'] not in old_node_ids:
            # Extract ID and name
            node_id = node['id']
            node_name = node.get('name', 'No name provided')  # Default if no name is available
            new_node_info.append(f"ID: {node_id}, Name: {node_name}")
    return new_node_info

# Function to save the extracted information to a text file
def save_to_text(data, filename):
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + '\n')

# Function to save JSON data to a file
def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load the JSON files
first_json = load_json('dsg_obj_backend_run1.json')
second_json = load_json('dsg_obj_backend_run2.json')

# Find new nodes and extract their ID and name
added_node_info = find_and_extract_new_nodes(first_json, second_json)

# Save the new node information to a text file
save_to_text(added_node_info, 'added_nodes_info.txt')'''
import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_to_text_file(data, file_path):
    with open(file_path, 'w') as file:
        for line in data:
            file.write(f"{line}\n")


def get_comparison_key(node):
    # Extracts the 'id', 'position', and 'name' from the node's 'attributes', converting 'position' to a tuple
    return (
        node.get('id'),
        tuple(node.get('attributes', {}).get('position', [])),  # Convert 'position' to a tuple
        node.get('attributes', {}).get('name')
    )

def process_files(file1_path, file2_path, output_file_path, text_file1, text_file2, added_nodes_file):
    graph1 = load_json(file1_path)
    graph2 = load_json(file2_path)

    # Create dictionaries with comparison keys for both graphs
    keys1 = {get_comparison_key(node): node for node in graph1['nodes']}
    keys2 = {get_comparison_key(node): node for node in graph2['nodes']}

    # Identify added or changed nodes in graph2
    added_or_changed_nodes = []
    for key, node in keys2.items():
        if key not in keys1:
            added_or_changed_nodes.append(node)

    # Change color of added or changed nodes to green in graph2 and save the modified graph
    for node in added_or_changed_nodes:
        if 'attributes' in node:
            node['attributes']['color'] = [0, 255, 0]  # RGB for green

    with open(output_file_path, 'w') as file:
        json.dump(graph2, file, indent=4)

  # Save nodes and their comparison keys to text files
    save_to_text_file([f"ID: {key[0]}, Position: {key[1]}, Name: {key[2]}" for key in keys1.keys()], text_file1)
    save_to_text_file([f"ID: {key[0]}, Position: {key[1]}, Name: {key[2]}" for key in keys2.keys()], text_file2)
    save_to_text_file([f"ID: {get_comparison_key(node)[0]}, Position: {get_comparison_key(node)[1]}, Name: {get_comparison_key(node)[2]}" for node in added_or_changed_nodes], added_nodes_file)

    # Save nodes and their comparison keys to text files
    '''save_to_text_file([f"ID: {key[0]}, Name: {key[1]}" for key in keys1], text_file1)
    save_to_text_file([f"ID: {key[0]}, Name: {key[1]}" for key in keys2], text_file2)
    save_to_text_file([f"ID: {key[0]}, Name: {key[1]}" for key in added_keys], added_nodes_file)
'''


    # Find added nodes in graph2
    #added_nodes = {id: node for id, node in nodes2.items() if id not in nodes1}





# Usage
file1_path = 'dsg_backend_run1.json'
file2_path = 'dsg_backend_run2.json'
output_file_path = 'modified_dsg_back.json'
text_file1 = 'nodes_file1_b_r1.txt'
text_file2 = 'nodes_file2_b_r2.txt'
added_nodes_file = 'added_nodes_b.txt'

if __name__ == '__main__':
    process_files(file1_path, file2_path, output_file_path, text_file1, text_file2, added_nodes_file)
