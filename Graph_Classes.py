from matplotlib import pyplot as plt
import networkx as nx
from itertools import combinations
import random as rd
import numpy as np

""" Node Class """

class Node:
    # Class that represents a node in a graph.
    def __init__(self, id: int, weight: float = 0, value: float = 0, parent = None, children: list = []) -> None:
        self.id = id
        self.weight = weight
        self.value = value
        self.neighbours = []
        self.parent  = parent
        self. children = children

    # returns 
    def Get_Neighbours(self, node_id: bool = False):
        if node_id:
            return [node.id for node in self.neighbours]
        return self.neighbours
    
    # returns 
    def Get_Children(self, child_id: bool = False):
        if child_id:
            return [node.id for node in self.children]
        return self.children

""" Edge Class """

class Edge:
    # Class that will represent the edges in a graph.
    def __init__(self, parent: Node, child: Node, tree: bool = False, direction: int = 0, weight: float = 0) -> None:
        self.parent = parent
        self.child = child 
        self.tree = tree
        self.direction = direction
        self.weight = weight
        self.Add_Neighbours()
        if self.tree: self.Add_Tree_Relation() 
    
    # adding the nodes to the neighbours lists.
    def Add_Neighbours(self):
        self.parent.neighbours.append(self.child)
        self.child.neighbours.append(self.parent)

    # if you are working with a tree graph, this will be used to add the relations.
    def Add_Tree_Relation(self):
        self.parent.children.append(self.child)
        self.child.parent = self.parent
    
    def Return_Attributes(self):
        return [self.parent, self.child, self.weight, self.direction]

""" Main Graph Class """

class Super_Graph:
    # Superclass of graphs.
    def __init__(self, name: str, vertices: list = [], edges: list = []) -> None:
        self.name = name 
        self.vertices = vertices
        self.edges = edges
    
    def Get_Vertex_IDs(self):
        return [v.id for v in self.vertices]
    
    def Get_Edge_IDs(self):
        return [(e.parent.id, e.child.id) for e in self.edges]

    # prints the vertices and edges to the console.
    def Rep_Attributes(self):
        vertices_names = self.Get_Vertex_IDs()
        edges_names = self.Get_Edge_IDs()

        print(f"Number of Vertices: {len(vertices_names)} and number of Edges: {len(edges_names)}.")
        print(f"Vertices: {vertices_names}\nEdges:")
        for e in edges_names:
            print(f"{e[0]} --- {e[1]}")

""" Ordinary Graph Class """

class Graph(Super_Graph):
    def __init__(self, name: str, vertices: list = [], edges: list = []) -> None:
        super().__init__(name, vertices, edges)

    # Add a vertex to the graph if its id is not yet in the graph. 
    def Add_Vertex(self, vertex: Node):
        if vertex.id not in self.Get_Vertex_IDs():
            self.vertices.append(vertex)
        else:
            print(f"Vertex {vertex.id} already in {self.name}.\n")
            return None

    # Add an edge to the graph via two vertices, which have to be in self.vertices
    def Add_Edge(self, v_1: Node, v_2: Node, direction: int = 0, weight: float = 0):
        vertex_set = self.Get_Vertex_IDs()

        if v_1.id in vertex_set and v_2.id in vertex_set:
            self.edges.append(Edge(v_1, v_2, direction=direction, weight=weight))
        else:
            if v_1.id in vertex_set:
                print(f"Vertex {v_2.id} is not in {self.name}.\n")
            else:
                print(f"Vertex {v_1.id} is not in {self.name}.\n")
            return None

    # Return list of all vertex degrees either ordered or in the order of appearance.
    def Get_Degree_List(self, order: bool = False) -> list:
        degree_list = [(v, len(v.Get_Neighbours())) for v in self.vertices]
        if order: 
            return sorted(degree_list, key=lambda x: x[1])
        return degree_list

    def Random_Graph(self, num_vertices: int = 10) -> None:
        # Choose random values regarding # edges.
        e_max = int(0.5*num_vertices*(num_vertices - 1)) # Max number of edges in a clique with v_rnd vertices.
        e_rnd = rd.randint(0, e_max)

        # Creating Nodes for the graph.
        indices_list = range(0, num_vertices)
        vertex_test = [Node(i) for i in indices_list]
        for vertex in vertex_test:
            self.Add_Vertex(vertex)
        
        # Create list of all possible edges.
        edges_test = list(combinations(indices_list, 2))
        edges_test = rd.sample(edges_test, k=e_rnd)

        # Add random edges to the graph.
        for edge in edges_test:
            self.Add_Edge(vertex_test[edge[0]], vertex_test[edge[1]])

    # plot the graph.
    def Draw_Graph(self):
        # Get all the needed nodes and edges from the entered graph.
        node_set = self.Get_Vertex_IDs()
        edge_set = self.Get_Edge_IDs()
        
        draw_graph = nx.DiGraph()
        draw_graph.add_nodes_from(node_set)
        draw_graph.add_edges_from(edge_set)

        pos = nx.spring_layout(draw_graph)
        nx.draw_networkx_nodes(draw_graph, pos, node_size=400)
        nx.draw_networkx_labels(draw_graph, pos)
        nx.draw_networkx_edges(draw_graph, pos, arrows=False)
        plt.show()

""" Tree Class """

class Tree(Super_Graph):
    def __init__(self, name: str, root: Node = None, vertices: list = [], edges: list = []) -> None:
        super().__init__(name, vertices, edges)
        self.root = root
        self.vertices.append(root)
    
    # add a node as a leaf to the tree.
    def Add_Leaf(self, parent: Node,  child: Node, weight: float = 0):
        if parent in self.vertices:
            self.vertices.append(child)
            self.edges.append(Edge(parent, child, True, weight=weight))
        else:
            print(f"Vertex {parent.id} not in Tree.")
            return None
    
    "error when running (15,4), only adds 12 nodes."
    # create a random tree of size # max_vertices.
    def Randomize_Tree(self, max_vertices: int = 10, max_children: int = 2):
        vertices_append = [Node(i, children=[]) for i in range(0, max_vertices)]

        # define the root of the tree.
        self.root = vertices_append[0]
        self.vertices = [vertices_append[0]]
        vertices_append.pop(0)

        # variables for the while loop, prev_child. contains the children from the current level of the tree, next_child. contains the next children to be worked on.
        current_node = self.root
        previous_children, next_children = [], []

        while len(vertices_append) > 0:
            # randomize the number of children.
            rnd_children = rd.randint(1,max_children)
            if rnd_children < len(vertices_append):
                # add children to the current vertex.
                for i in range(0, rnd_children):
                    print(f"--> {current_node.id} {vertices_append[0].id}")
                    self.Add_Leaf(current_node, vertices_append[0])
                    vertices_append.pop(0)

                next_children = [*next_children, *current_node.children]

                # if there are still unvisited nodes on the current level.
                if len(previous_children) > 0:
                    current_node = previous_children[0]
                    previous_children.pop(0)
                # case if all nodes on the current level have been visited.
                else:
                    current_node = next_children[0]
                    previous_children = next_children[1:]
                    next_children = []
            # case if there are less than rnd_children left to be added.
            else:
                for item in vertices_append:
                    self.Add_Leaf(current_node, item)
                vertices_append = []
    
    # to be added.
    def Get_Height(self):
        pass
    
    # to be added.
    def Draw_Tree(self):
        pass


if __name__ == "__main__":
    #v_1, v_2, v_3 = Node(1), Node(2), Node(3) 
    #e_1, e_2 = Edge(v_1, v_2), Edge(v_1, v_3)
    #test_super_graph = Graph("test graph", [v_1, v_2, v_3], [e_1, e_2])
    #test_super_graph.Rep_Attributes()

    #test_graph = Graph("test randomize")
    #test_graph.Random_Graph(5)
    #test_graph.Rep_Attributes()
    #test_graph.Draw_Graph()

    #n_1, n_2, n_3, n_4 = Node(1), Node(2), Node(3), Node(4)
    #test_tree = Tree("test tree", n_1)
    #test_tree.Add_Leaf(n_1, n_2)
    #test_tree.Add_Leaf(n_1, n_3)
    #test_tree.Add_Leaf(n_3, n_4)
    #test_tree.Rep_Attributes()

    test_tree_random = Tree("test randomize")
    test_tree_random.Randomize_Tree(15, 4)
