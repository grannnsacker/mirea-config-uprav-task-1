class Tree:
    class Node:
        def __init__(self, path, is_dir):
            self.children = []
            self.parent = None
            self.is_directory = is_dir
            self.path = path

        def __str__(self):
            return str(self.path)

        def add_children(self, name, is_dir):
            children_node = Tree.Node(self.path + '/' + name, is_dir)
            children_node.parent = self
            children_node.is_directory = is_dir
            #children_node.path =  #+ ('/' if children_node.is_directory else '')
            self.children.append(children_node)
            #print(f"||{children_node}, {children_node.parent}, {children_node.path}||")

    def __init__(self, name):
        self.root = self.Node(name, True)

    def print_tree(self, node):
        if node.path:
            print(node.path)
        for i in node.children:
            self.print_tree(i)

    def get_node_by_path(self, path) -> Node:
        if path == "root":
            return self.root
        current_node = self.root
        path_list = path.split("/")[1:]
        for step in path_list:
            for child in current_node.children:
                if step in child.path.split("/"):
                    current_node = child
                if current_node.path == path:
                    return current_node

    def add_node(self, parent_path, self_name, is_dir):
        elem = self.get_node_by_path(parent_path)
        if elem:
            elem.add_children(self_name, is_dir)




