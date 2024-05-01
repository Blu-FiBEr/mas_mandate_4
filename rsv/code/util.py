import matplotlib.pyplot as plt
import numpy as np
import datetime
import os


# Initializing folder configurations for log and results of the simulations.

today = datetime.datetime.now()
sim_folder = "Simulation-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "-" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)
path = os.getcwd()
allsim_path = path+"/Simulations/"
sim_path = path+"/Simulations/"+sim_folder
src_path = path+"/Simulations/"+sim_folder+"/src"
if not os.path.isdir(allsim_path):
    os.mkdir(allsim_path)
os.mkdir(sim_path)
os.mkdir(src_path)

log_file = sim_path + "/log.txt"
log_enabled = True


def my_print(text):
    """
        Write in the log file and in the screen.
    """
    text = str(text)
    datetime_str = str(datetime.datetime.now())
    try:
        if log_enabled:
            file = open(log_file, "a")
            file.write(datetime_str+"; "+text+"\n")
            file.close()
        print(datetime_str+"; "+text+"\n")
    except IOError as error:
        print("IO Error." + str(error))


def plot_simple_unit_count(population, na, nra, method, detailed_result_m, detailed_result_RSm):
    method_text = ""
    if method == 1:
        method_text = "Borda"
    elif method == 2:
        method_text = "Plurality"
    elif method == 3:
        method_text = "Approval"
    elif method == 4:
        method_text = "Condorcet"

    xs = range(1, population + 1)
    plt.clf()
    for dm in detailed_result_m:
        plt.xlabel('# voters')
        plt.ylabel('count')
        plt.subplot(1, 2, 1)
        plt.plot(xs, detailed_result_m[dm])
        plt.title(method_text)

        plt.subplot(1, 2, 2)
        plt.plot(xs, detailed_result_RSm[dm])
        plt.title('RS' + str(nra))

    folder = sim_path+"/SimpleUnit"
    os.makedirs(folder)
    filename = folder + "/" + "plot-unit.png"

    plt.savefig(filename)


def plot_simple_unit_mi(population, na, nra, method, mi2_evolution_m, mi2_evolution_rs):
    method_text = ""
    if method == 1:
        method_text = "Borda"
    elif method == 2:
        method_text = "Plurality"
    elif method == 3:
        method_text = "Approval"
    elif method == 4:
        method_text = "Condorcet"

    xs = range(1, population + 1)
    plt.clf()
    plt.xlabel('# voters')
    plt.ylabel('count')
    x = [i for i in range(1,population+1)]
    fig, ax = plt.subplots()
    mi2_m_line, = ax.plot(x, mi2_evolution_m, label="MI2 - "+method_text)
    mi2_rs_line, = ax.plot(x, mi2_evolution_rs, label="MI2 - "+method_text)

    plt.title(method_text)

    folder = sim_path+"/SimpleUnit"
    filename = folder + "/" + "plot-unit-mi2.png"

    plt.savefig(filename)


def gaussian(x, mu, sig):
    """
        Returns the image of the gaussian function
    """
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def draw_gauss(means, sigma):
    """
        Draws the gaussian distributions in the file gauss.png
    """
    folder = sim_path + "/" + "Create-scenario"

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError as error:
        print("Error creating directory" + str(error))
    xs = np.linspace(-2, 3, 100)
    plt.clf()
    for mean in means:
        ys = [gaussian(x, mean, sigma) for x in xs]
        plt.plot(xs, ys, label="N("+str(round(mean, 2))+","+str(sigma)+")")
    plt.legend()
    plt.xlabel("Mean")
    filename = folder+"/gauss.png"
    plt.savefig(filename)


def draw_first_place_distribution(alternatives, dms):
    """
        Save a histogram of the first place for the alternatives.
    """

    # this dic will register the histogram.
    # Since we had some issues with the matplotlib.hist,
    # we decided to explicitly calculate the histogram

    folder = sim_path + "/" + "Create-scenario"

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError as error:
        print("Error creating directory" + str(error))

    dic = {}
    for a in alternatives:
        # We need to set 0.1 because of the bar function.
        # It does not plot zeros.
        dic[a] = 0.1
    for dm in dms:
        fp = dm['list'][0]
        dic[fp] += 1

    # fp_list = []
    # for dm in dms:
    #    fp_list.append(dm['list'][0])
    # x = plt.hist(fp_list, bins=N)

    plt.clf()
    plt.xlabel('Alternative')
    plt.ylabel('Number of votes')
    plt.bar(dic.keys(), dic.values())
    filename = folder+"/fp_dist_"+str(len(alternatives))+"_"+str(len(dms))+".png"
    plt.savefig(filename)
    # plt.show()


def method_text(method):
    if method == 1:
        return "Borda"
    elif method == 2:
        return "Plurality"
    elif method == 3:
        return "Approval"
    elif method == 4:
        return "Copeland"
