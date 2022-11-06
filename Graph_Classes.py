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
    
    