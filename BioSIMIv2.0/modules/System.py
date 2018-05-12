from modules.Subsystem import *

class System(object):
    def __init__(self, SystemName):
        self.SystemName = SystemName

    def getSystemName(self):
        return self.SystemName

    def setSharedResources(self, ListOfResources):
        return

    def createSubsystem(self, filename, subsystemName):
    # 1. Read the SBML model
    # 2. Create an object of the Subsystem class with the SBMLDocument read in Step 1
        name = self.getSystemName()
        sbmlDoc = getFromXML(filename)
        subsystem = Subsystem(sbmlDoc)
        subsystem.suffixAllElementIds(subsystemName)
        if sbmlDoc.getModel().getNumCompartments() > 1:
            print('More than 1 compartments in the model')
        subsystem.setSubsystemCompartments([name])
        return subsystem 
