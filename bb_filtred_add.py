import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_to_text_file(data, file_path):
    with open(file_path, 'w') as file:
        for line in data:
            file.write(f"{line}\n")

def get_comparison_key(node):
    # Extracts the 'id', 'position', 'name', and 'bounding_box' from the node's 'attributes'
    return (
        node.get('id'),
        tuple(node.get('attributes', {}).get('position', [])),  # Convert 'position' to a tuple
        node.get('attributes', {}).get('name'),
        node.get('attributes', {}).get('bounding_box')  # Bounding box as a dictionary
    )

def has_required_attributes(node):
    # Checks if the node has 'id', 'position', 'name', and 'bounding_box' in its 'attributes'
    attributes = node.get('attributes', {})
    return 'id' in node and all(key in attributes for key in ['position', 'name', 'bounding_box'])

def compare_nodes(node1, node2):
    # Compare nodes based on name, id, position, and bounding_box
    if node1.get('attributes', {}).get('name') != node2.get('attributes', {}).get('name'):
        return False  # Names are different
    if node1.get('id') != node2.get('id'):
        # IDs are different, check position and bounding_box
        return node1.get('attributes', {}).get('position') == node2.get('attributes', {}).get('position') and \
               node1.get('attributes', {}).get('bounding_box') == node2.get('attributes', {}).get('bounding_box')
    # IDs are the same, check for changes in position or bounding box
    return node1.get('attributes', {}).get('position') == node2.get('attributes', {}).get('position') and \
           node1.get('attributes', {}).get('bounding_box') == node2.get('attributes', {}).get('bounding_box')

def process_files(file1_path, file2_path, output_file_path, text_file1, text_file2, added_nodes_file):
    graph1 = load_json(file1_path)
    graph2 = load_json(file2_path)

    # Filter nodes with required attributes and create lists
    filtered_nodes1 = list(filter(has_required_attributes, graph1['nodes']))
    filtered_nodes2 = list(filter(has_required_attributes, graph2['nodes']))

    # Identify added or changed nodes in graph2
    added_or_changed_nodes = [node for node in filtered_nodes2 if not any(compare_nodes(node, node1) for node1 in filtered_nodes1)]

    # Change color of added or changed nodes to green in graph2 and save the modified graph
    for node in added_or_changed_nodes:
        if 'attributes' in node:
            node['attributes']['color'] = [0, 255, 0]  # RGB for green

    with open(output_file_path, 'w') as file:
        json.dump(graph2, file, indent=4)

    # Save nodes and their IDs, positions, names, and bounding boxes to text files
    save_to_text_file([f"ID: {node['id']}, Position: {get_comparison_key(node)[1]}, Name: {get_comparison_key(node)[2]}, Bounding Box: {get_comparison_key(node)[3]}" for node in filtered_nodes1], text_file1)
    save_to_text_file([f"ID: {node['id']}, Position: {get_comparison_key(node)[1]}, Name: {get_comparison_key(node)[2]}, Bounding Box: {get_comparison_key(node)[3]}" for node in filtered_nodes2], text_file2)
    save_to_text_file([f"ID: {node['id']}, Position: {get_comparison_key(node)[1]}, Name: {get_comparison_key(node)[2]}" for node in added_or_changed_nodes], added_nodes_file)

# File paths (replace with actual paths)
file1_path = 'dsg_obj_backend_run1.json'
file2_path = 'dsg_obj_backend_run2.json'
output_file_path = 'modified_dsg_obj_backend_run2.json'
text_file1 = 'nodes_file1.txt'
text_file2 = 'nodes_file2.txt'
added_nodes_file = 'added_nodes_filtered_bb.txt'

if __name__ == '__main__':
    process_files(file1_path, file2_path, output_file_path, text_file1, text_file2, added_nodes_file)
