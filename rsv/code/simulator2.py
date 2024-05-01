#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
# CFixed the display problem on AWS (Amazon Servers)
matplotlib.use('Agg')

import random
import datetime
import shutil
import util
import basics
import param


def match_index(dict):
    """
        Count the matches comparing a dictionary with a list.
        Dict: {1: 35, 2: 36, 3: 14, 5: 20, 6: 10}
        Each key is the alternative and the value is the count so far.
        List to be compared to the expected result 1,2,3,4...
        Parameter: dictionary. Not a list.
    """
    criteria = 0
    base_result = [x for x in range(1,len(dict)+1)]

    sorted_tuples = sorted(dict.items(), key=lambda dict: dict[1], reverse=True)
    i=0
    for count in sorted_tuples:
        if count[0] == base_result[i]:
            criteria +=1
        i+=1
    return criteria


def match_index2(list1):
    """
        Count the matches between two lists.
        The list1 is the argument in the format: [1,4,3,5,...]
        The second one is the list [1,2,3,4,5....]
        The expected result according to the scenario creation model.
    """
    criteria = 0
    list2 = [x for x in range(1, len(list1) + 1)]
    for c in range(len(list1)):
        if list1[c] == list2[c]:
            criteria +=1
    return criteria


def sort_list(original, sample):
    """
        This method works as follows:
        ([4,7,2,1,6,9,10] and [6,10,4]) ---> [4,6,10]
        It orders the sample list based on the order of the original list.
    """
    ordered_sample = []
    for i in original:
        if i in sample:
            ordered_sample.append(i)
    return ordered_sample


def compute_basic(method_unit, dms, nra):
    """
    12/07/2019
    This method is a basic version of the compute_plus.
    The difference is that compute_basic only outputs the final aggregate ranking.
    The evolution of the count and of the MI is not. We hope for more performance in this method.
    Computes the result of the voting.
    :param method_unit: Borda (1), Plurality (2), Approval (3), Condorcet (4)
    :param dms: dict of decision makers
    :param nra: number of random alternatives
    :return:
    """
    # result is a dictionary:
    # 1: 20, 2: 10, 3: 13.
    # we compute the votes or score for each alternative.
    result = {}

    #initializes the result dictionary
    for alt in dms[0]['list']:
        result[alt] = 0

    for d in dms:
        # d['list'] is the list of preferences of the voter d
        # Example: [4,1,3,2]
        random_subset = random.sample(d['list'], nra)
        rank = sort_list(d['list'], random_subset)
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
    return aggregated_ranking


def compute_plus(method_unit, dms, nra):
    """
    Computes the result of the voting.
    :param method_unit: Borda (1), Plurality (2), Approval (3), Condorcet (4)
    :param dms: dict of decision makers
    :param nra: number of random alternatives
    :return:
    """
    # result is a dictionary:
    # 1: 20, 2: 10, 3: 13.
    # we compute the votes or score for each alternative.
    result = {}

    # stores the evolution of the score for each alternative.
    # 1: [2, 4, 7, 10..], 2: [1, 2, 5, 6...]
    # this variable will be used to draw the graph of the evolution of the scores as the voters cast their votes.
    detailed_result = {}

    # stores the evolution of the mi2.
    # We call mi2 the count matches between the method and the expected result, i.e, 1,2,3,4,5..
    # since we have defined the rules of the simulation in a way that 1,2,3,4... is the expected result,
    # we simply evaluate how close the method is to the expected result.
    # It is simply a list.
    mi2_evolution = []

    #initializes the result dictionary
    for alt in dms[0]['list']:
        result[alt] = 0

    for alt in dms[0]['list']:
        detailed_result[alt] = []

    for d in dms:
        # d['list'] is the list of preferences of the voter d
        # Example: [4,1,3,2]
        random_subset = random.sample(d['list'], nra)
        rank = sort_list(d['list'], random_subset)
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

        for item in result:
            detailed_result[item].append(result[item])

        # note that the variable result is a dictionaty with each element as a key.
        # the values are the count of each alternative.
        # in the function match_index2 a list, no a dict, is the parameter.
        # I have then transformed result into result_list.
        #result_list = [i for i in result.keys()]
        mi2 = match_index(result)
        mi2_evolution.append(mi2)

    sorted_results = sorted(result.items(), key=lambda results: results[1], reverse=True)
    aggregated_ranking = [x[0] for x in sorted_results]
    return aggregated_ranking, detailed_result, mi2_evolution


def compute_copeland(dms, nra):
    """
    12/07/2019
    Computes the result of the voting: Copeland method
    :param method_unit: Borda (1), Plurality (2), Approval (3), Condorcet (4)
    :param dms: dict of decision makers
    :param nra: number of random alternatives
    :return:

    VIDEO: https://photos.google.com/photo/AF1QipNzUU7HdbB1LT1YD6apTdx2FvGOorAz8p4hKojI
    In this video, I detail how the copeland method works and how it was implemented.
    """
    # result is a dictionary:
    # 1: 20, 2: 10, 3: 13.
    # we compute the votes or score for each alternative.
    result = {}

    # The copeland matrix
    copeland_matrix = []

    # number of alternatives
    na = len(dms[0]['list'])

    # initializes the result dictionary
    for alt in range(1,na+1):
        result[alt] = 0

    # initializes the copeland matrix
    for i in range(0, na+1):
        line = []
        line.append(i)
        for j in range(1, na + 1):
            if i==0:
                line.append(j)
            else:
                line.append(0)
        copeland_matrix.append(line)

    # computes
    for d in dms:
        # d['list'] is the list of preferences of the voter d
        # Example: [4,1,3,2]
        random_subset = random.sample(d['list'], nra)
        rank = sort_list(d['list'], random_subset)
        # note that the rank can be the full ranking or the RSranking of the voter.
        # when nra = na we will have the full ranking, i.e. the original method.

        for i in range(1, na):
            for j in range(i+1, na+1):
                if i in rank and j in rank:
                    if rank.index(i) < rank.index(j): # i is prefered to j
                        copeland_matrix[i][j] += 1
                    else: # j is prefered to i
                        copeland_matrix[j][i] += 1
                elif i in rank and j not in rank:
                    copeland_matrix[i][j] += 1
                elif i not in rank and j in rank:
                    copeland_matrix[j][i] += 1
                else: # in case i and j not in rank, which means that they are not in the RS, no points for them
                    # I have explicitly used pass for readability
                    pass


    for i in range(1, na):
        for j in range(i+1, na+1):
            if copeland_matrix[i][j] > copeland_matrix[j][i]:
                result[i] +=1
            elif copeland_matrix[i][j] < copeland_matrix[j][i]:
                result[j] += 1
            else:
                result[i] += 0.5
                result[j] += 0.5

    sorted_results = sorted(result.items(), key=lambda results: results[1], reverse=True)
    aggregated_ranking = [x[0] for x in sorted_results]
    return aggregated_ranking


def simulate_unit(population, na, nra, method):
    """

    :param method: The voting method:  1 for Borda, 2 for plurality, 3 for approval, 4 for Condorcet.
    :return: ?
    """

    dms = basics.create_scenario(population, na)
    rankingm, detailed_result_m, mi2_evolution_m = compute_plus(method, dms, na)
    rankingRSm, detailed_result_RSm, mi2_evolution_rs = compute_plus(method, dms, nra)
    mi_m = match_index2(rankingm)
    mi_rs = match_index2(rankingRSm)
    print("MI - method: "+str(mi_m))
    print("MI - RS: "+str(mi_rs))

    util.plot_simple_unit_count(population, na, nra, method, detailed_result_m, detailed_result_RSm)
    util.plot_simple_unit_mi(population, na, nra, method, mi2_evolution_m, mi2_evolution_rs)


def test_simulate_copeland(population, na, nra):
    """

    :param method: The voting method:  1 for Borda, 2 for plurality, 3 for approval, 4 for Condorcet.
    :return: ?
    """

    dms = basics.create_scenario(population, na)
    rankingm = compute_copeland(dms, nra)
    mi_m = match_index2(rankingm)
    print("MI - method: "+str(mi_m))


def simulate_multir_multimethod():
    scenarios = [(5000, 10), (6000, 10)]
    methods = [2]
    runs = 50

    str_rs = ""
    for i in range(2, 11):
        str_rs = str_rs + str(i)+";"

    util.my_print("Time;Scenario;Method;run;r;"+str_rs)
    for scenario in scenarios:
        for method in methods:
            n = scenario[0]
            na = scenario[1]
            for run in range(0, runs):
                mis_str = ""
                for r in range(2, na+1):
                    dms = basics.create_scenario(n, na)
                    if method in [1,2,3]:
                        final_ranking = compute_basic(method, dms, r)
                    else:
                        final_ranking = compute_copeland(dms, r)
                    mi = match_index2(final_ranking)
                    mis_str = mis_str + str(mi) + ";"
                time = str(datetime.datetime.now())

                util.my_print(time+";" + str(scenario) + ";" + util.method_text(method) + ";" + \
                              str(run) + ";-; " + mis_str)


def simulate_multimethod_increase_n(na, r_list, n_max):
    methods = [1, 2, 3, 4]
    increment = 2000
    runs = 2

    util.my_print("m;n;r;Borda;Plurality;Approval;Condorcet")
    for r in r_list:
        for n in range(200, n_max + 1, increment):
            mis_str = ""
            for method in methods:
                sum_mi = 0
                for run in range(runs):
                    dms = basics.create_scenario(n, na)
                    if method in [1, 2, 3]:
                        final_ranking = compute_basic(method, dms, r)
                    else:
                        final_ranking = compute_copeland(dms, r)
                    sum_mi += match_index2(final_ranking)
                mi = sum_mi / runs
                mis_str = mis_str + str(mi) + ";"
            util.my_print(str(na) + ";" + str(n) + ";" + str(r) + ";" + mis_str)


def main():
    # PARAMETERS AND FOLDER SETUP
    # os.makedirs(base_folder)
    # replicates the simulator.py file on the created folder.

    shutil.copy(util.path + "/basics.py", util.sim_path + "/src/basics.py")
    shutil.copy(util.path + "/simulator2.py", util.sim_path + "/src/simulator2.py")
    shutil.copy(util.path + "/util.py", util.sim_path + "/src/util.py")

    simulations = param.simulations
    print(simulations)
    for sim in simulations:
        na = sim[0]
        r_list = sim[1]
        n_max = sim[2]
        simulate_multimethod_increase_n(na, r_list, n_max)


if __name__ == '__main__':
    main()
