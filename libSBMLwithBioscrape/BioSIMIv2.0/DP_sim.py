#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl

#%config InlineBackend.figure_f.ormats=['svg']

mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))

mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12)


import numpy as np

# Code for simple gene expression without delay

# Import relevant types
from bioscrape.types import Model
from bioscrape.simulator import DeterministicSimulator, SSASimulator
from bioscrape.simulator import ModelCSimInterface

# Load the model by creating a model with the file name containing the model
m = Model('DP.xml')
# Expose the model's core characteristics for simulation. (i.e. stoichiometry,
# delays, and propensities)
s = ModelCSimInterface(m)

s.py_set_initial_time(0)

# This function uses sparsity to further optimize the speed of deterministic
# simulations. You must call it before doing deterministic simulations.
s.py_prep_deterministic_simulation()

# Set up our desired timepoints for which to simulate. 
# Must match with initial time.
timepoints = np.linspace(0,100,1000)

# Create a DeterministicSimulator as well as an SSASimulator
ssa_simulator = SSASimulator()
det_simulator = DeterministicSimulator()

# Simulate the model with both simulators for the desired timepoints
stoch_result = ssa_simulator.py_simulate(s,timepoints)
det_result = det_simulator.py_simulate(s,timepoints)

# Process the simulation output.

# py_get_result() returns a numpy 2d array of timepoints x species.
# Each row is one time point and each column is a species.
# stoch_sim_output = stoch_result.py_get_result()
det_sim_output = det_result.py_get_result()

# Get the indices for each species of interest

# From the model, we can recover which column corresponds to which species, so
# we then know which column of the result array is which species.

in_ind = m.get_species_index('in')
out_ind = m.get_species_index('out')
# protein_ind = m.get_species_index('protein')

# Plot the mRNA levels over time for both deterministic and stochastic simulation

# plt.plot(timepoints,stoch_sim_output[:,out_ind])
plt.plot(timepoints,det_sim_output[:,out_ind])
plt.plot(timepoints,det_sim_output[:,in_ind])
plt.xlabel('Time')
plt.ylabel('out')
plt.show()

# plt.figure()
# # prot_ind = m.get_species_index('protein')
# # plt.plot(timepoints,stoch_sim_output[:,in_ind])
# plt.plot(timepoints,det_sim_output[:,in_ind])
# plt.xlabel('Time')
# plt.ylabel('input')
# plt.show()