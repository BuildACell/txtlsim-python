from libsbml import *
from ayushCode import modules

reader = SBMLReader()
doc_DP1 = reader.readSBML('DP1.sbml')
model_DP1 = doc_DP1.getModel()
DP1_subsystem = Subsystem(model_DP1)

doc_DP2 = reader.readSBML('DP2.sbml')
model_DP2 = doc_DP2.getModel()
DP2_subsystem = Subsystem(model_DP2)

doc_IFFL = reader.readSBML('IFFL.sbml')
model_IFFL = doc_IFFL.getModel()
IFFL_Subsystem = Subsystem(model_IFFL)

Final_sbml_doc = SBMLDocument(3,1)
final_model = Final_sbml_doc.createModel()
Final_subsystem = Subsystem(final_model)

connection_logic = {}
connection_logic['DP1_out'] = 'IFFL_pA'
connection_logic['DP2_out'] = 'IFFL_pB'

Final_subsystem.connect([DP_Subsystem1, DP_Subsystem2],[IFFL_Subsystem], connection_logic)






