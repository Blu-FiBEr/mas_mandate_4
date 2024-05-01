import random
from graph import Graph
from vertex import Vertex
from edge import Edge


class Policy:
    def __init__(self, graph, epsilon = 0.7, empty = False):
        self.epsilon = epsilon
        self.graph = graph
        self.policy = {}  # Dictionary to store policy for each vertex
        # self.policy_particles = init_count
        
        if(empty): return
        # Initialize policy for each vertex
        for vertex_name in self.graph.vertices.keys():
            # self.policy[vertex_name] = {}
            neighbors = self.graph.get_neighbors(Vertex(vertex_name))
            
            if (neighbors == None or len(neighbors) == 0):
                self.policy[vertex_name] = None
            
            else: self.policy[vertex_name] = random.choice(neighbors)
            # num_neighbors = len(neighbors)
            # self.policy[vertex_name]["total"] = num_neighbors * init_count
            # if num_neighbors > 0:
            #     count_per_action = init_count
            #     for neighbor in neighbors:
            #         self.policy[vertex_name][neighbor] = count_per_action
            # else:
            #     # If vertex has no neighbors, assign equal probability to stay in the same vertex
            #     self.policy[vertex_name][vertex_name] = 1
            

    def get_policy(self):
        """
        Get the policy structure.
        """
        return self.policy

    def choose_action(self, vertex, arg_max = 0):
        """
        Choose one of the neighbors of a given vertex using the counts array of the vertex.
        """
        neighbors = self.graph.get_neighbors(Vertex(vertex.name))
        # intermediate.remove("total")
        # neighbors = intermediate
        if(neighbors == None or len(neighbors) == 0) : 
            return None
        # probabilities = list(self.policy[vertex.name].values())
        if (random.random() < self.epsilon):
            chosen_neighbor = self.policy[vertex.name]

        else: 
            # probabilities = [(self.policy[vertex.name][neighb]/self.policy[vertex.name]["total"]) for neighb in neighbors]
            chosen_neighbor = random.choice(neighbors)

        if (arg_max == 1):
            # chosen_neighbor = max(neighbors, key=lambda n: self.policy[vertex.name][n] / self.policy[vertex.name]["total"])
            chosen_neighbor = self.policy[vertex.name]

        return chosen_neighbor
    
    # def update_count(self, vertex_1, vertex_2, prob, delta):
    #     if(vertex_1.name == vertex_2.name): return

    #     if(random.random() > prob): return
        
    #     initial_count = self.policy[vertex_1.name][vertex_2.name]
        
    #     self.policy[vertex_1.name][vertex_2.name] += delta
    #     if(self.policy[vertex_1.name][vertex_2.name] < self.policy_particles):
    #         self.policy[vertex_1.name][vertex_2.name] = self.policy_particles

    #     self.policy[vertex_1.name]["total"] += self.policy[vertex_1.name][vertex_2.name] - initial_count

    #     return
