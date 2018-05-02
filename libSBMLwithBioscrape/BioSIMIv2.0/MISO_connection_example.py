#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl

#%config InlineBackend.figure_f.ormats=['svg']

mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))

mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12)


import numpy as np


from libsbml import *
import libsbml
from modules.Subsystem import *
from modules.NewReaction import *

reader = SBMLReader()
doc_DP1 = reader.readSBML('models/DP1_sbml.xml')
DP1_subsystem = Subsystem(doc_DP1)

doc_DP2 = reader.readSBML('models/DP2_sbml.xml')
DP2_subsystem = Subsystem(doc_DP2)

doc_IFFL = reader.readSBML('models/IFFL_sbmlNew.xml')
IFFL_Subsystem = Subsystem(doc_IFFL)

final_sbml_doc = SBMLDocument(3,1)
# DP1_model = doc_DP1.getModel()
check(final_sbml_doc.createModel(),'setting model of final doc')
# print(final_sbml_doc.getModel())
Final_subsystem = Subsystem(final_sbml_doc)

connection_logic = {}
connection_logic["out_DP1"] = "pA_IFFL"
connection_logic["out_DP2"] = "pB_IFFL"


# Final_subsystem.connect([DP1_subsystem, DP2_subsystem],[IFFL_Subsystem], connection_logic)
# Final_subsystem.connect(DP1_subsystem,IFFL_Subsystem, connection_logic)

#add simulate and plot 

# Write SBML file in XML
# writeSBML(Final_subsystem.getNewDocument(),'models/DP_IFFL_connected.xml')

# Simulate 
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/DP_IFFL_connected_hardcoded.xml')
s = bioscrape.simulator.ModelCSimInterface(m)
s.py_prep_deterministic_simulation()
s.py_set_initial_time(0)

inp_DP1_ind = m.get_species_index('inp_DP1')
inp_DP2_ind = m.get_species_index('inp_DP2')
out_IFFL_ind = m.get_species_index('out_IFFL')
sim = bioscrape.simulator.DeterministicSimulator()
timepoints = np.linspace(0,10,1000)
result = sim.py_simulate(s,timepoints)
# print(result.py_get_result()[1])
plt.xlabel('Time')
plt.ylabel('input/output species')
plt.plot(timepoints,result.py_get_result()[:,inp_DP1_ind])
plt.plot(timepoints,result.py_get_result()[:,inp_DP2_ind])
plt.plot(timepoints,result.py_get_result()[:,out_IFFL_ind])
plt.legend([m.get_species_list()[inp_DP1_ind],m.get_species_list()[inp_DP2_ind],m.get_species_list()[out_IFFL_ind]])

# plt.plot(timepoints,result.py_get_result())
# plt.plot(timepoints,result.py_get_result())
plt.show()