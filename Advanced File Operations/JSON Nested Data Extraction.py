import json
import re
import time

# Tree node class
class TreeNode:
    def __init__(self, name, data=None, parent_path=None):
        self.name = name
        self.children = []
        self.data = data  # Only product nodes have data
        self.path = (parent_path or []) + [name]

# Build tree recursively
def build_tree(obj, name="root", parent_path=None):
    node = TreeNode(name, parent_path=parent_path)

    if isinstance(obj, dict):
        for key, value in obj.items():
            child = build_tree(value, key, node.path)
            node.children.append(child)
    elif isinstance(obj, list):
        for item in obj:
            child = TreeNode("product", item, node.path)
            node.children.append(child)

    return node

# DFS search
def dfs_search(node, matches, pattern, min_price):
    global nodes_traversed
    nodes_traversed += 1

    if node.data:  # Leaf node (product)
        product = node.data
        try:
            if (
                product.get("price", 0) > min_price and
                re.search(pattern, product.get("id", ""))
            ):
                matches.append((node.path, product))
        except:
            pass

    for child in node.children:
        dfs_search(child, matches, pattern, min_price)

# Calculate depth
def get_tree_depth(node):
    if not node.children:
        return 1
    return 1 + max(get_tree_depth(child) for child in node.children)

# ---- Main Program ----
def main():
    json_file = "product_catalog.json"  # Replace with your file if needed
    try:
        with open(json_file) as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
        return

    # Build the tree
    tree = build_tree(data)

    # Search
    global nodes_traversed
    matches = []
    nodes_traversed = 0
    start = time.time()
    dfs_search(tree, matches, r"(LP|DT)", 1000)
    end = time.time()

    # Output results
    for path, product in matches:
        print(f"Category path: {' > '.join(path[1:])}")
        print(f"- {product['id']}: {product['name']} (${product['price']})")
        if "specs" in product:
            specs = ", ".join(f"{k.upper()}: {v}" for k, v in product["specs"].items())
            print(f"Specs: {specs}")
        print()

    print(f"Total matches found: {len(matches)}")
    print(f"Search time: {round(end - start, 3)} seconds")
    print(f"Tree depth: {get_tree_depth(tree)}")
    print(f"Nodes traversed: {nodes_traversed}")

if __name__ == "__main__":
    main()
