import threading
import random
from agent import Agent
from vertex import Vertex
from policy import Policy
import multiprocessing
GENERATION_SIZE = 200
EPSILON = 0.4


class MAS:
    def __init__(self, graph, num_agents):
        self.graph = graph
        self.max_heuristics = {vertex_name : (self.graph.num_vertices * self.graph.max_weight) for vertex_name in self.graph.vertices.keys()}
        self.num_agents = num_agents
        self.agents = []
        for _ in range(0, num_agents):
            self.agents.append(Agent(self))
        # self.policy = policy
        # self.best_policy = policy
        self.policy_dict = {} # mapping from integer to policy
        for i in range(GENERATION_SIZE):
            random_policy = Policy(self.graph, EPSILON)
            self.policy_dict[str(i)] = random_policy
        self.best_policy = self.policy_dict["0"]


    # def set_policy(self, policy):
    #     """
    #     Set the policy for the MAS.
    #     """
    #     self.policy = policy

    def run_agents(self, max_len, num_episodes):
        """
        Run each agent in a separate thread with their initial position.
        """
        threads = []
        for id, agent in enumerate(self.agents):
            thread = threading.Thread(target=self._run_agent, args=(agent, max_len, num_episodes, id))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def agent_rank_wrapper(self,args):
        agent, alloc_candidates = args
        return agent.get_ranks(alloc_candidates)

    def run_voting_all(self, nra, method_unit=1):
        # result is a dictionary:
        # 1: 20, 2: 10, 3: 13.
        # we compute the votes or score for each alternative.
        agents = self.agents
        result = {}
        alt_list = list(self.policy_dict.keys())

        #initializes the result dictionary
        for alt in alt_list:
            result[alt] = 0

        alloc_candidates = []


        for _ in agents:
            alloc_candidates.append(random.sample(alt_list, nra))
        
        agent_alloc_pairs = zip(agents, alloc_candidates)
        pool = multiprocessing.Pool()
        agent_prefs = pool.map(self.agent_rank_wrapper, agent_alloc_pairs)
        pool.close()
        pool.join()

        for rank in agent_prefs:

            # d['list'] is the list of preferences of the voter d
            # Example: [4,1,3,2]
            # random_subset = random.sample(d['list'], nra)
            # rank = sort_list(d['list'], random_subset)
            # rank = 
            # note that the rank can be the full ranking or the RSranking of the voter.
            # when nra = na we will have the full ranking, i.e. the original method.
            if method_unit ==1: #Borda
                for i in range(nra):
                    result[rank[i]] += nra-i

            if method_unit==2: #plurality
                result[rank[0]] += 1

            if method_unit==3: #approval
                # s is the number of alternatives that will be approved by the voter.
                #s = random.randint(1,len(rank))
                if len(rank) ==2:
                    s=1
                elif len(rank) <=5:
                    s=2
                else:
                    s=4
                for i in range(s):
                    result[rank[i]] += 1


        sorted_results = sorted(result.items(), key=lambda results: results[1], reverse=True)
        aggregated_ranking = [x[0] for x in sorted_results]
        final_rank_dict = {aggregated_ranking[i] : (i + 1) for i in range(len(aggregated_ranking))}
        self.best_policy = self.policy_dict[aggregated_ranking[0]]

        # Final order of policy names (strings)
        return final_rank_dict
    
    def evolution(self, reproduction_module, final_rank_dict):
        self.policy_dict = reproduction_module.policy_switching(self.policy_dict, final_rank_dict, self.graph)
        self.policy_dict["0"] = self.best_policy
        # print(self.policy_dict)
        

    def _run_agent(self, agent, max_len, num_episodes, id):
        """
        Internal method to run an agent with its initial position.
        """

        # run multiple episodes.
        # update after each episode ends.
        part_len = (self.graph.num_vertices) // self.num_agents
        for _ in range(0, num_episodes):
            if(id != self.num_agents - 1):
                agent.initial_position = random.choice(list(self.graph.vertices.keys())[id * part_len :(id + 1) * part_len])
            else:
                agent.initial_position = random.choice(list(self.graph.vertices.keys())[id * part_len:])
            # agent.initial_position = random.choice(list(self.graph.vertices.keys()))
            agent.current_position = Vertex(agent.initial_position)
            agent.episode(max_len)
            agent.update()
            # Implement agent behavior here based on policy
            # For example, choose an action based on policy and update agent's position
            # action = self.policy.choose_action(agent.current_position)
            # agent.update(action)
            # pass  # Placeholder implementation

    def add_agent(self, agent):
        """
        Add an agent to the MAS.
        """
        self.agents.append(agent)

    
    def test_policy(self, max_len):
        test_distances = {}
        test_distances[self.graph.goal_vertex.name] = 0
        for i in (self.graph.vertices):
            if(i == self.graph.goal_vertex.name): continue
            current_position = Vertex(i)
            trajectory = []
            total_dist = 0
            while (len(trajectory) < max_len and (len(trajectory) == 0 or trajectory[len(trajectory)-1][2] != None)):
                if current_position.name == self.graph.goal_vertex.name:
                    break  # Agent reached the goal

                # Sample action from random policy
                action = self.best_policy.choose_action(current_position, arg_max = 1)
                if (action == None):
                    trajectory.append(
                        (current_position, current_position, None))
                    total_dist = float('inf')
                    break
                next_state = Vertex(action)
                # Append (s, a, r) pair to trajectory
                trajectory.append(
                    (current_position, next_state, self.graph.get_edge_weight(current_position, next_state)))
                total_dist += self.graph.get_edge_weight(current_position, next_state)

                # Sample next state from transitions
                # Update current position
                current_position = next_state
            if(len(trajectory) >= max_len): total_dist = float('inf')
            test_distances[i] = total_dist
        
        differences = {}
        num_differences = 0
        abs_diff_sum = 0

        # Check keys in dict1
        for key in test_distances:
            # if key not in dict2:
            #     differences[key] = (dict1[key], None)
            #     num_differences += 1
            if test_distances[key] != self.graph.dijkstra_distances[key]:
                differences[key] = (test_distances[key], self.graph.dijkstra_distances[key])
                num_differences += 1
                margin = abs(test_distances[key] - self.graph.dijkstra_distances[key])
                if(margin == float('inf')): 
                    margin = 0
                    num_differences -= 1
                abs_diff_sum += margin
        avg_loss = 0
        if(num_differences != 0): avg_loss = (abs_diff_sum/num_differences)
        return differences, num_differences, avg_loss, test_distances
