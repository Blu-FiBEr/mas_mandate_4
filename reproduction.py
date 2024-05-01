import random
from graph import Graph
from vertex import Vertex
from edge import Edge
from policy import Policy
import numpy as np
from mas import GENERATION_SIZE
from mas import EPSILON
PARENT_SIZE = 10
GLOBAL_MUTATE_PROB = 0.3  # Keep less
GLOBAL_MUTATE = 0.8
LOCAL_MUTATE = 0.4


class Reproduction:
    def policy_switching(self, policy_dict, final_rank_dict, graph):
        new_policy_dict = {}
        for i in range(GENERATION_SIZE - 1):
            parent_group = random.sample(
                list(final_rank_dict.keys()), PARENT_SIZE)
            new_born = self.mate_mutate(parent_group, policy_dict,
                                        final_rank_dict, graph)
            new_policy_dict[str(i + 1)] = new_born
        return new_policy_dict

    def mate_mutate(self, parent_group,  policy_dict, final_rank_dict, graph):
        weights = [(final_rank_dict[policy_name])
                   for policy_name in parent_group]
        # print(weights)
        weights = self.normalize_list(weights)
        # print(weights)
        new_born = Policy(graph, EPSILON,  empty=True)
        glob_mutation_marker = 0
        if (random.random() < GLOBAL_MUTATE_PROB):
            glob_mutation_marker = 1
        for vertex_name in graph.vertices.keys():
            # Choose an index according to the probabilities
            chromosome_num = np.random.choice(len(parent_group), p=weights)
            chromosome_policy = policy_dict[parent_group[chromosome_num]]
            # print(new_born, chromosome_policy)
            new_born.policy[vertex_name] = chromosome_policy.policy[vertex_name]

            # Mutation

            if (glob_mutation_marker == 1 and random.random() < GLOBAL_MUTATE):
                neighbors = graph.get_neighbors(Vertex(vertex_name))

                if (neighbors == None or len(neighbors) == 0):
                    new_born.policy[vertex_name] = None
                else:
                    new_born.policy[vertex_name] = random.choice(neighbors)

            elif (random.random() < LOCAL_MUTATE):
                neighbors = graph.get_neighbors(Vertex(vertex_name))

                if (neighbors == None or len(neighbors) == 0):
                    new_born.policy[vertex_name] = None
                else:
                    new_born.policy[vertex_name] = random.choice(neighbors)

        return new_born

    def normalize_list(self, input_list):
        # Convert the input list to a NumPy array
        original_array = np.array(input_list)

        # Compute the reciprocal square root of each element
        # reciprocal_sqrt_array = 1 / np.sqrt(original_array)
        reciprocal_sqrt_array = 1 / original_array

        # Normalize the array so that the sum is 1
        normalized_array = reciprocal_sqrt_array / \
            np.sum(reciprocal_sqrt_array)

        # Convert the normalized array back to a Python list
        normalized_list = normalized_array.tolist()

        return normalized_list
