#!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 18/03/2014

from collections import defaultdict

##
# The following class is based on/adapted from the open source work by Lynn Root, http://gist.github.com/econchick/4666413.
##
  
"""
"" @name: Graph (Class)
"" @author: Daniel Koehler
"" @description: Class to handle the creation of Graphs and finding shortest paths through them
"""

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}


    """
    "" @name: Add Node
    "" @author: Daniel Koehler  
    "" @description: Method to add a node to this instance of a graph
    "" @prams: Node handle
    "" @return: void
    """
 
    def add_node(self, value):
        self.nodes.add(value)

    """
    "" @name: Add edge
    "" @author: Daniel Koehler  
    "" @description: Method to add an edge between two nodes
    "" @prams: none
    "" @return: void
    """
 
    def add_edge(self, from_node, to_node, distance):
        # Add to edges from both directions so we can use either key
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

        # Add to distances from both directions so we can use either key
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance
    
    """
    "" @name: Group Popover (Message Box)
    "" @author: Daniel Koehler  
    "" @description: Method to display a popup allowing a group to be added
    "" @prams: none
    "" @return: void
    """

    def dijsktra(self, initial, end):

        # Visted Nodes
        visited = {initial: 0}
        # Path container to return
        path = {}
        # Python set of nodea - useful because we can perform intersections on the set
        nodes = set(self.nodes)
        
        # While we haven't seen all nodes
        while nodes:
            # Min distance from initial
            min_node = None
            # Loop over nodes
            for node in nodes:
                # If we haven't seen this node
                if node in visited:
                    # if the min distance has never been set
                    if min_node is None:
                        # Set to first node
                        min_node = node
                    # Else set node only if it has a short distance
                    elif visited[node] < visited[min_node]:
                        min_node = node
            
            # There were no unvisited nodes
            if min_node is None:
                break
            
            # Remove node 
            nodes.remove(min_node)
            current_weight = visited[min_node]
            
            for edge in self.edges[min_node]:
                weight = current_weight + self.distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
        
        return visited[end]



