import random
from vertex import Vertex


class Agent:
    def __init__(self, mas, initial_position=None):
        self.initial_position = initial_position
        self.current_position = initial_position
        self.mas = mas
        self.trajectory = []

    def episode(self, max_len,  policy=None):
        """
        Perform an episode for the agent until it reaches the goal or maximum length is reached.
        """
        if (policy == None):
            print("none_policy_given")
        self.trajectory = []

        self.current_position = Vertex(self.initial_position)
        while (len(self.trajectory) < max_len and (len(self.trajectory) == 0 or self.trajectory[len(self.trajectory)-1][2] != None)):
            # print(self.current_position.name)
            # print("traj: " + str(len(self.trajectory)))
            if self.current_position.name == self.mas.graph.goal_vertex.name:
                break  # Agent reached the goal

            # Sample action from random policy
            action = policy.choose_action(self.current_position)
            # print("action: " + str(action))
            if (action == None):
                self.trajectory.append(
                    (self.current_position, self.current_position, None))
                # print(self.current_position.name)
                break
            next_state = Vertex(action)
            # Append (s, a, r) pair to trajectory
            self.trajectory.append(
                (self.current_position, next_state, self.mas.graph.get_edge_weight(self.current_position, next_state)))

            # Sample next state from transitions
            # Update current position
            self.current_position = next_state

        # Perform update for all agents that have not reached but max_len reached
        # self.update()

    # def update(self, payoff_constant=5, update_delta=15, neg_prob=0.7, neg_delta=5):
    #     """
    #     Update policy using trajectory
    #     """
    #     traj = self.trajectory
    #     # if(len(traj) > 1): print(len(traj))

    #     if (len(traj) == 0 and self.current_position.name == self.mas.graph.goal_vertex.name):
    #         return
    #     # print(self.initial_position + "--" + self.mas.graph.goal_vertex.name + "--" + traj[len(traj) - 1][1].name)
    #     if (traj[len(traj) - 1][1].name == self.mas.graph.goal_vertex.name):
    #         # print("snacd,")
    #         path_len = 0
    #         for i in reversed(range(len(traj))):
    #             path_len += traj[i][2]
    #             prev_best = self.mas.max_heuristics[traj[i][0].name]
    #             # print("cbjs")
    #             if (path_len <= prev_best):
    #                 payoff = (prev_best + payoff_constant - path_len)/(prev_best +
    #                                                                    payoff_constant - self.mas.graph.heuristic[traj[i][0].name])
    #                 update_prob = payoff
    #                 self.mas.max_heuristics[traj[i][0].name] = path_len

    #                 self.mas.policy.update_count(
    #                     traj[i][0], traj[i][1], update_prob, update_delta)

    #     else:
    #         update_prob = neg_prob
    #         for i in (range(len(traj))):
    #             self.mas.policy.update_count(
    #                 traj[i][0], traj[i][1], update_prob, -neg_delta)

    #     return

        # pass  # This method will be implemented later

    def get_ranks(self, alloc_candidates):
        # make max_ep_len a keyword arg
        temp = self.mas.graph.goal_vertex.name
        while (temp == self.mas.graph.goal_vertex.name):
            temp = random.choice(
                list(self.mas.graph.vertices.keys()))

        self.initial_position = temp

        max_ep_len = self.mas.graph.num_vertices
        results = []
        for curr_policy in alloc_candidates:
            traj_len = 0
            while (traj_len <= 0):

                self.episode(
                    10 * max_ep_len, policy=self.mas.policy_dict[curr_policy])

                traj_len = len(self.trajectory)

            # print(self.trajectory[traj_len - 1])
            if (self.trajectory[traj_len - 1][1].name == self.mas.graph.goal_vertex.name):
                results.append((curr_policy, traj_len))
            else:
                results.append((curr_policy, float('inf')))

        rank = [x[0]
                for x in sorted(results, key=lambda x: x[1], reverse=True)]

        # rank is an oredered list of policies (the string names of policies)
        return rank
