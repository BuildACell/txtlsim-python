import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.System import *

cell = System('cell')

A0 = cell.createSubsystem('models/A0.xml','A0')
writeSBML(A0.getSubsystemDoc(),'models/A0converted.xml')
# Simulate using bioscrape
timepoints = np.linspace(0,14*60*60,1000)

plotSbmlWithBioscrape('models/A0converted.xml',0,
timepoints,['protein deGFP*','protein sigma28'],'Time',
'concentration (nM)',14,14)
