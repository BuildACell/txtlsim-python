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
# from bioscrape.types import Model
# from bioscrape.simulator import DeterministicSimulator, SSASimulator
# from bioscrape.simulator import ModelCSimInterface

from libsbml import *
import simplesbml
import libsbml 

model = simplesbml.sbmlModel()
model.addCompartment(1e-14, comp_id='comp')
model.addSpecies('E', 5e-21, comp='comp')
model.addSpecies('S', 1e-20, comp='comp')
model.addSpecies('P', 0.0, comp='comp')
model.addSpecies('ES', 0.0, comp='comp')
model.addParameter('koff', 0.2)
model.addParameter('kon', 1000000.0)
model.addParameter('kcat', 0.1)
model.addReaction(['E', 'S'], ['ES'], 'comp*(kon*E*S-koff*ES)', rxn_id='veq')
model.addReaction(['ES'], ['E', 'P'], 'comp*kcat*ES', rxn_id='vcat')

modelforXML = model.getDocument()
# writeSBML(modelforXML,"models/simpleExample.xml")
# To convert SBML from any level and version to any other level and version
# Currently, the file simpleExampleXML.xml is in L3 V1..
# make your SBMLDocument type document from the XML file

# reader = SBMLReader()
# document = reader.readSBML("models/simpleExampleXML.xml")

# # Use document.getLevel() and document.getVersion() to check...
# # many other checks can be done with different member functions documented on sbml.org
# # Use document.checkL2v4compatibility() to check 
# # if "document" (the SBMLDocument object you created above) is compatible with level 2 v 4
# # Now, Create a ConversionsProperties() object as follows
# config = ConversionProperties()
# # Many options can be added to the ConversionProperties object (config - that we created)
# # Of our interest in the option of conversion to a different level and version. 
# if config != None:
#     config.addOption('setLevelAndVersion')
#     # Now, we need to set the target level and version (to which we want to convert the document)
#     # Use the setTargetNamespaces() object of the ConversionsProperties as follows.
#     # First, we need to create a new SBMLNamespaces object with the desired (target) level and version
#     sbmlns = SBMLNamespaces(2,4)
#     config.setTargetNamespaces(sbmlns)
#     # Use the SBMLDocument.convert(ConversionsProperties) syntax to convert
#     status = document.convert(config)
#     # Check if status is successfull or not
#     if status != LIBSBML_OPERATION_SUCCESS:
#       # Handle error
#        print('Error: unable to strip the Layout package.')
#        print('LibSBML returned error: ' + OperationReturnValue_toString(status).strip())
# else:
#     print('Error: unable to create ConversionProperties object')
# print(document.getLevel())
# # Write the converted SBMLDocument to a new XML file
# # You may check document.getLevel() and so on to be additionally ensured that conversion was successful
# writeSBML(document,"models/ConvertedToLevel2.xml")

# print(modelforXML) >> 'simpleExampleXML.xml'
# code = simplesbml.writeCodeFromString(model.toSBML())
# print(code)
# code1 = simplesbml.writeCode(model.document) #Produces code to create model 'example' in string format
# print(model.document)
# print(document.getNumErrors())
# model = document.getModel()
# print(model.getNumSpecies())
# document.libsbml.SBMLDocument.checkConsistency()
# document.libsbml.SBMLDocument.checkL2v2Compatibility()

# import bioscrape
# m = bioscrape.types.read_model_from_sbml('models/ConvertedToLevel2.xml')
# s = bioscrape.simulator.ModelCSimInterface(m)
# s.py_prep_deterministic_simulation()
# s.py_set_initial_time(0)

# sim = bioscrape.simulator.DeterministicSimulator()
# timepoints = np.linspace(0,100,1000)
# result = sim.py_simulate(s,timepoints)
# plt.plot(timepoints,result.py_get_result())
# plt.legend(m.get_species_list())
# plt.show()