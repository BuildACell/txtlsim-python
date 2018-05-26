import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.System import *

cell = System('cell')
cell.ListOfSharedResources = ['RNAP','Ribo','ATP']

A1 = cell.createSubsystem('models/A1.xml','A1')
writeSBML(A1.getSubsystemDoc(),'models/A1converted.xml')
# Simulate using bioscrape
timepoints = np.linspace(0,14*60*6000,1000)

plotSbmlWithBioscrape('models/A1converted.xml',0,
timepoints,['protein deGFP*','protein sigma28'],'Time',
'concentration (nM)',14,14)
