from libsbml import *

reader = SBMLReader()
doc_DP1 = reader.readSBML('DP1.xml')
model_DP1 = doc_DP1.getModel()
DP1_subsystem = Subsystem(model_DP1)

doc_DP2 = reader.readSBML('DP2.sbml')
model_DP2 = doc_DP2.getModel()
DP2_subsystem = Subsystem(model_DP2)

doc_IFFL = reader.readSBML('IFFL.sbml')
model_IFFL = doc_IFFL.getModel()
IFFL_Subsystem = Subsystem(model_IFFL)

# final_sbml_doc = SBMLDocument(3,1)
try:
   final_sbml_doc = SBMLDocument(3, 1)
except ValueError:
   print('Could not create SBMLDocument object')
   sys.exit(1)
 
final_subsystem = Subsystem(final_sbml_doc)
final_model = final_subsystem.createNewModel("seconds","mole","count")

connection_logic = {}
connection_logic['DP1_out'] = 'IFFL_pA'
connection_logic['DP2_out'] = 'IFFL_pB'

Final_subsystem.connect([DP_Subsystem1, DP_Subsystem2],[IFFL_Subsystem], connection_logic)






