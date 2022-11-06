from matplotlib import pyplot as plt
import networkx as nx
import random as rd
import numpy as np


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



class Graph:
    # Superclass of graphs.
    def __init__(self, name: str, vertices: list = [], edges: list = []) -> None:
        self.name = name 
        self.vertices = vertices
        self.edges = edges
    
    def Get_Vertex_IDs(self):
        return [v.id for v in self.vertices]
    
    def Get_Edge_IDs(self):
        return [(e.parent.id, e.child.id) for e in self.edges]

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

    # prints the vertices and edges to the console.
    def Rep_Attributes(self, node_id: bool = False):
        vertices_names = self.Get_Vertex_IDs(node_id = node_id)
        edges_names = self.Get_Edge_IDs(node_id = node_id)

        print(f"Number of Vertices: {len(vertices_names)} and number of Edges: {len(edges_names)}.")
        print(f"Vertices: {vertices_names}\nEdges:")
        for e in edges_names:
            print(f"{e[0]} --- {e[1]}")


class Tree(Graph):
    def __init__(self, name: str, root: Node, vertices: list = [], edges: list = []) -> None:
        super().__init__(name, vertices, edges)
        self.root = root
    
    def Add_Leaf(self, parent: Node,  child: Node):
        pass

    def Get_Height(self):
        pass





if __name__ == "__main__":
    v_1, v_2, v_3 = Node(1), Node(2), Node(3)
    test_graph = Graph("test graph")
    test_graph.Add_Vertex(v_1)
    test_graph.Add_Vertex(v_2)

    test_graph.Add_Edge(v_1, v_2)

    print(test_graph.Get_Degree_List(True))

