#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
# CFixed the display problem on AWS (Amazon Servers)
matplotlib.use('Agg')

import numpy as np
import random
import util
import shutil


def create_alternatives(number_of_alternatives):
    """
        Creates a list of alternatives based on the required number of alternatives.
        We represent the list of alternatives as a list of numbers:
        [1,2,3,4,5...]
        Each item in the list is a positive integer.

    """
    list_of_alternatives = range(1, number_of_alternatives + 1)
    return list_of_alternatives


def create_decisionmakers(number_of_decisionmakers, list_of_alternatives, folder):
    """
        Creates a random list of decisionmakers (DMs)
        Each item in the list is a dictionary with an id, representing the DM id, and a list, representing the order
        stablished by the DM for all alternatives.
        Parameters:
        Base curve:
            1: (2-np.sqrt(4-4*(x-1)**2))/2 ;
            2: 1-x**(0.5) ;
            3: 1-x
            4: 1-x**2
            5: np.sqrt(1-x**2)
        Interval: [0,1]
        Distribution: Gauss
        Mean: Equally distributed in the interval
        Sigma: 0.5
    """

    sigma = 0.5
    x_exp = np.linspace(0, 1, len(list_of_alternatives))
    means = [f(3, x) for x in x_exp]
    list_of_decisionmakers = []
    for i in range(1, number_of_decisionmakers + 1):
        dic = {}
        dic['id'] = i
        list_copy = list_of_alternatives[:]
        dic['list'] = shuffle_alternatives(list_copy, number_of_decisionmakers, means, sigma)
        # print str(i)
        list_of_decisionmakers.append(dic)

    # util.draw_gauss(means, sigma, folder)
    # util.draw_first_place_distribution(list_of_alternatives, list_of_decisionmakers, folder)
    return list_of_decisionmakers


def create_scenario(number_of_decisionmakers, number_of_alternatives):
    """
        Creates a random list of decisionmakers (DMs)
        Each item in the list is a dictionary with an id, representing the DM id, and a list, representing the order
        stablished by the DM for all alternatives.
        Parameters:
        Base curve:
            1: (2-np.sqrt(4-4*(x-1)**2))/2 ;
            2: 1-x**(0.5) ;
            3: 1-x
            4: 1-x**2
            5: np.sqrt(1-x**2)
        Interval: [0,1]
        Distribution: Gauss
        Mean: Equally distributed in the interval
        Sigma: 0.5
    """
    # util.my_print("Creating scenario ("+str(number_of_decisionmakers)+","+str(number_of_alternatives)+")")
    list_of_alternatives = range(1, number_of_alternatives + 1)  # for example: [1,2,3,4...]
    sigma = 0.5  # the std dev of the gaussian that will be used
    x_exp = np.linspace(0, 1, len(list_of_alternatives))
    means = [f(3, x) for x in x_exp]
    list_of_decisionmakers = []
    for i in range(1, number_of_decisionmakers + 1):
        dic = {}
        dic['id'] = i
        list_copy = list_of_alternatives[:]
        dic['list'] = shuffle_alternatives(list_copy, number_of_decisionmakers, means, sigma)
        list_of_decisionmakers.append(dic)

    util.draw_gauss(means, sigma)
    util.draw_first_place_distribution(list_of_alternatives, list_of_decisionmakers)
    return list_of_decisionmakers


def f(opt, x):
    """
        Calculate the image of x according to the chosen function.

    """
    if opt == 1:
        return (2 - np.sqrt(4 - 4 * (x - 1) ** 2)) / 2
    elif opt == 2:
        return 1 - x ** (0.5)
    elif opt == 3:
        return 1 - x
    elif opt == 4:
        return 1 - x ** 2
    elif opt == 5:
        return np.sqrt(1 - x ** 2)


def shuffle_alternatives(alternatives_list, number_of_decisionmakers, means, sigma):
    """
        Shuffle a list of alternatives according to a specific randomization process.
        For every element in the list we generate a random (gaussian) number, with increasing mean
        starting from zero.
    """
    results = {}
    count = 0
    for element in alternatives_list:
        mean = means[count]
        results[element] = random.gauss(mean, sigma)
        count += 1

    sorted_results = sorted(results.items(), key=lambda results: results[1], reverse=True)
    return [x[0] for x in sorted_results]


def main():
    """
    This main is only used to test the scenario creation methods implemented in this package.
    :return:
    """
    shutil.copy(util.path + "/scenario.py", util.sim_path + "/src/scenario.py")
    shutil.copy(util.path + "/simulator2.py", util.sim_path + "/src/simulator2.py")
    shutil.copy(util.path + "/util.py", util.sim_path + "/src/util.py")
    create_scenario(10000,10)

if __name__ == '__main__':
    main()