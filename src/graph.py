# Daniela Vidal Canas, Student ID: 001172091
# Class vertex to create a grid of the city
class Vertex:
    def __init__(self, label):
        self.label = label
        self.visited = False


# Class graph to create a grid of the city with wighted edges
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_vertex_from_label(self, vertex_label):
        for adjacent in self.adjacency_list:
            if adjacent.label == vertex_label:
                return adjacent
