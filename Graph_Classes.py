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

    def get_neighbours(self, show: bool = False):
        if show:
            for node in self.neighbours:
                print(f"neighbour of {self.id}: {node.id}")
        return self.neighbours
    
    def get_children(self, show: bool = False):
        if show:
            for node in self.children:
                print(f"neighbour of {self.id}: {node.id}")
        return self.children
    
class Edge:
    def __init__(self, parent: Node, child: Node, direction: int = 0, weight: float = 0) -> None:
        self.parent = parent
        self.child = child 
        self.direction = direction
        self.weight = weight 
    
    def add_neighbours(self):
        self.parent.neighbours.append(self.child)
        self.child.neighbours.append(self.parent)

    def add_tree_relation(self):
        self.parent.children.append(self.child)
        self.child.parent = self.parent
    
    def return_attributes(self):
        return [self.parent, self.child, self.weight, self.direction]


