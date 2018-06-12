# Import all required libraries
from modules.Subsystem import * 

class System(object):
    def __init__(self, SystemName):
        self.SystemName = SystemName
        self.ListOfSubsystems = []
        self.ListOfSharedResources = []
    
    def getSystemName(self):
        ''' 
        Returns the system name attribute
        '''
        return self.SystemName

    def setSystemName(self, name):
        ''' 
        Renames the system name and puts all subsystems 
        currently in the system inside the compartment with 
        this new name 
        '''
        for subsystem in self.ListOfSubsystems:
            subsystem.setCompartments([name])
        self.SystemName = name

    def getListOfSubsystems(self):
        ''' 
        Returns the list of subsystem objects in 
        the system 
        '''
        return self.ListOfSubsystems
    
    def getListOfSharedResources(self):
        ''' 
        Returns the list of shared resources
        '''
        return self.ListOfSharedResources

    def appendSharedResources(self, list):
        ''' 
        Append the list of resources to the 
        self.ListOfSharedResources 
        '''
        for element in list:
            if type(element) is str: 
                self.ListOfSharedResources.append(element)
            else:
                raise ValueError('List element {0} is not a string'.format(element))
    
    def removeSharedResource(self, resource):
        ''' 
        Remove the given resource name from
        self.ListOfSharedResources
        '''
        if type(resource) is str and resource in self.ListOfSharedResources:
            self.ListOfSharedResources.remove(resource)

    def setSharedResources(self):
        ''' 
        Returns a new Subsystem object containing the 
        model which shares the self.ListOfSharedResources among 
        self.ListOfSubsystems
        '''
        ListOfResources = self.ListOfSharedResources
        # Create a blank document for the final connected system and the subsystem object
        final_sbml_doc = createSbmlDoc(3,1)
        Final_subsystem = Subsystem(final_sbml_doc)
        Final_subsystem.setSystem(self)
        # The shareSubsystems member function implements Example 1-A.
        # Usage - self.shareSubsystems(ListOfSubsystems, ListOfSharedResources)
        Final_subsystem.shareSubsystems(self.ListOfSubsystems, ListOfResources)
        return Final_subsystem

    def createSubsystem(self, filename, subsystemName = ''):
        ''' 
        Creates a new Subsystem object inside the System
        with the SubsystemName suffixed to all elements of the given SBML filename
        '''
    # 1. Read the SBML model
    # 2. Create an object of the Subsystem class with the SBMLDocument read in Step 1
        name = self.getSystemName()
        sbmlDoc = getFromXML(filename)
        subsystem = Subsystem(sbmlDoc)
        subsystem.setSystem(self)
        if subsystem.getSubsystemDoc().getLevel() != 3:
            print('Subsystem SBML model is not the latest. Converting to SBML level 3, version 1')
            subsystem.convertSubsystemLevelAndVersion(3,1)
        subsystem.suffixAllElementIds(subsystemName)
        if sbmlDoc.getModel().getNumCompartments() > 1:
            print('More than 1 compartments in the model')
        subsystem.setCompartments([name])
        # handling sbml events --- incomplete ---
        # model = subsystem.getSubsystemDoc().getModel()
        # if model.getNumEvents():
        #     for event in model.getListOfEvents()
        self.ListOfSubsystems.append(subsystem)
        return subsystem 

    def createNewSubsystem(self, level, version):
        '''
        Creates a new empty Subsystem object with SBMLDocument 
        of given level and version
        '''
        newDocument = createSbmlDoc(level,version)
        subsystem = Subsystem(newDocument)
        subsystem.setSystem(self)
        return subsystem

