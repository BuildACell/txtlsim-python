import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.System import *

cell = System('cell')
# cell.ListOfSharedResources = ['RNAP']
A0 = cell.createSubsystem('models/A0.xml','A0')
A1 = cell.createSubsystem('models/A1.xml','A1')
B0 = cell.createSubsystem('models/B0.xml','B0')
B1 = cell.createSubsystem('models/B1.xml','B1')

combined00 = cell.createNewSubsystem(3,1)
combined00.combineSubsystems([A0, B0],True)
writeSBML(combined00.getSubsystemDoc(),'models/combined00.xml')

combined01 = cell.createNewSubsystem(3,1)
combined01.combineSubsystems([A0,B1],True)
writeSBML(combined01.getSubsystemDoc(),'models/combined01.xml')

combined10 = cell.createNewSubsystem(3,1)
combined10.combineSubsystems([A1, B0],True)
writeSBML(combined10.getSubsystemDoc(),'models/combined10.xml')


combined11 = cell.createNewSubsystem(3,1)
combined11.combineSubsystems([A1, B1],True)
writeSBML(combined11.getSubsystemDoc(),'models/combined11.xml')


# Simulate using bioscrape
timepoints = np.linspace(0,55*60*6000)

plotSbmlWithBioscrape('models/combined00.xml',0,
# plotSbmlWithBioscrape('models/combined01.xml',0,
# plotSbmlWithBioscrape('models/combined10.xml',0,
# plotSbmlWithBioscrape('models/combined11.xml',0,
# plotSbmlWithBioscrape('combined11_mod.xml',0,
# plotSbmlWithBioscrape('models/connected11.xml',0,
timepoints,['protein deGFP*', 'protein tetRdimer'],'Time',
# timepoints,['protein deGFP*', 'protein tetRdimer', 'protein sigmaX'],'Time',
# timepoints,['protein deGFP*', 'protein tetRdimer', 'protein sigma28'],'Time',
# timepoints,['protein deGFP*','protein sigma28', 'protein sigmaX', 'protein tetRdimer'],'Time',
'concentration (nM)')
