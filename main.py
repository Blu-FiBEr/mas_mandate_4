from graph import Graph
from mas import MAS
# from policy import Policy
from reproduction import Reproduction


NUM_VERTICES = 5
NUM_EDGES = 20
MAX_WEIGHT = 10
NUM_AGENTS = 100
# POLICY_PARTICLES = 20
MAX_LEN = NUM_VERTICES
# NUM_EPISODES = 4
NUM_EPOCHS = 100
# EPSILON = 0.7
# GENERATION_SIZE = 200
# PARENT_SIZE = 20
# MUTATE_PROB = 0.2
VOTING_NRA = 50


main_graph = Graph(NUM_VERTICES, NUM_EDGES, MAX_WEIGHT)
main_mas = MAS(main_graph, NUM_AGENTS)
reproduction_module = Reproduction()

for i in range(NUM_EPOCHS):
    print("Epoch: " + str(i))
    final_ranks = main_mas.run_voting_all(nra=VOTING_NRA)
    main_mas.evolution(reproduction_module, final_ranks)
    print(main_mas.best_policy.policy)
    differences, _, avg_loss, _ = main_mas.test_policy(
        max_len=MAX_LEN)
    print(differences)
    print(avg_loss)

# differences, num_differences, avg_loss, test_distances = main_mas.test_policy(
#     max_len=MAX_LEN)
# print(differences)
# # print(test_distances)
# print(avg_loss)

# main_policy = Policy(main_graph, POLICY_PARTICLES)
# main_mas = MAS(main_graph, NUM_AGENTS, main_policy)


# def train(num_epochs):
#     for _ in range(0, num_epochs):
#         main_mas.run_agents(MAX_LEN, NUM_EPISODES)

# train(5)


# diffs, num_diffs, avg_loss, test_distances = main_mas.test_policy(MAX_LEN)

# print("Differences:", diffs)
# print("Number of differences:", num_diffs)
# print("Avg_loss:", avg_loss)
# print("Goal: " + main_graph.goal_vertex.name)
# print(test_distances)


# print(main_mas.policy.policy)

# def find_differences(dict1, dict2):
#     differences = {}
#     num_differences = 0

#     # Check keys in dict1
#     for key in dict1:
#         if key not in dict2:
#             differences[key] = (dict1[key], None)
#             num_differences += 1
#         elif dict1[key] != dict2[key]:
#             differences[key] = (dict1[key], dict2[key])
#             num_differences += 1

#     # Check keys in dict2 not in dict1
#     for key in dict2:
#         if key not in dict1:
#             differences[key] = (None, dict2[key])
#             num_differences += 1

#     return differences, num_differences


# # print(main_graph.vertices)

# dict1 = main_mas.test_policy(MAX_LEN)
# dict2 = main_graph.dijkstra_distances
# # print(dict2)

# diffs, num_diffs = find_differences(dict1, dict2)
