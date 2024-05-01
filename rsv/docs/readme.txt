Project: Simulator 2.1

This python project implements the simulation of Random-Subset Voting for:
- Borda,
- plurality,
- approval,
- Condorcet (Copeland).

The project contains 5 files:
- simulator2.py: is the main file of the project. 
- basics.py: contains the functions that create the random scenarios for the elections.
- util.py: contains the functions for printing and plotting.
- test.py: contains a few functions for testing the application.
- param.py: contains the parameters of the simulation.

The parameters are already set according to the paper submitted to JASSS in Aug/2019.
However, feel free to set the parameters in param.py in order to change:
- The number of alternatives
- The number of random alternatives
- The max population.

The version of python used is 3.2. The program requires two external libraries:
- matplotlib
- numpy.

In order to run the system, simply download it and run:
> python3 simulator2.py
The system will create a folder called Simulations in which all the simulations executed will the stored.
Each simulation registers a log, a csv file, in which the results are stored.
The lines in the log indicates:
- Time, 
- Number of alternatives
- Number of voters
- Number of random alternatives
- Result for Borda
- Result for Plurality
- Result for Approval
- Result for Condorcet

For example:
2019-08-02 17:52:06.325832; m;n;r;Borda;Plurality;Approval;Condorcet
2019-08-02 17:52:08.232093; 10;200;2;2.5;2.5;2.5;1.5;

In this run, 10 alternatives were tested in a population of 200 with 2 random alternatives.
The results of Borda, Plurality, approval and Condorcet were: 2.5, 2.5, 2.5, 1.5.

