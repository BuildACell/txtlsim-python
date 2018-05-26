# Import all required libraries
import bioscrape
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
        final_sbml_doc = createSubsystemDoc(3,1)
        Final_subsystem = Subsystem(final_sbml_doc)
        Final_subsystem.setSystem(self)
        # The shareSubsystems member function implements Example 1-A.
        # Usage - self.shareSubsystems(ListOfSubsystems, ListOfSharedResources)
        Final_subsystem.shareSubsystems(self.ListOfSubsystems, ListOfResources)
        return Final_subsystem

    def createSubsystem(self, filename, subsystemName):
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
        newDocument = createSubsystemDoc(level,version)
        subsystem = Subsystem(newDocument)
        subsystem.setSystem(self)
        return subsystem


def getFromXML(filename):
    """ 
    Returns the SBMLDocument object from XML file given 
    """

    reader = SBMLReader()
    doc = reader.readSBML(filename)
    check(doc, "reading from SBML file")
    return doc

def createSubsystemDoc(newLevel, newVersion):
    ''' 
    Creates a new SBMLDocument ojbect of the given newLevel and newVersion
    '''
    try:
        sbmlDoc = SBMLDocument(newLevel, newVersion)
    except ValueError:
        print('Could not create SBMLDocument object')
        sys.exit(1)
    return sbmlDoc

def plotSbmlWithBioscrape(filename, initialTime, timepoints, ListOfSpeciesToPlot, xlabel = 'Time', ylabel = 'Concentration (AU)', sizeOfXLabels = 14, sizeOfYLabels = 14):
    ''' 
    Plots the amounts of ListOfSpeciesToPlot in the given SBML filename
    starting at initialTime and for the timepoints given. 
    The other arguments for axes labels and sizes are optional
    '''
    mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))
    mpl.rc('xtick', labelsize=sizeOfXLabels) 
    mpl.rc('ytick', labelsize=sizeOfYLabels)
    doc = getFromXML(filename)
    model = doc.getModel()
    mod_obj = SimpleModel(model)
    m = bioscrape.types.read_model_from_sbml(filename)
    s = bioscrape.simulator.ModelCSimInterface(m)
    s.py_prep_deterministic_simulation()
    s.py_set_initial_time(initialTime)
    species_ind = []
    SpeciesToPlot = ListOfSpeciesToPlot[:]
    for i in range(len(ListOfSpeciesToPlot)):
        species_name = ListOfSpeciesToPlot[i]
        species = mod_obj.getSpeciesByName(species_name)
        if type(species) is list:
            print('There are multiple species with the name ' + species_name + ' in plot function. Suffixed species will be plotted ')
            for species_i in species:
                species_ind.append(m.get_species_index(species_i.getId()))
            key_ind = ListOfSpeciesToPlot.index(species_name)
            insert_new = []
            for i in range(len(species)-1):
                insert_new.append(species_name + str(i+1))
            SpeciesToPlot[key_ind+1:key_ind+1] = insert_new 
        else:
            species_ind.append(m.get_species_index(species.getId()))
    sim = bioscrape.simulator.DeterministicSimulator()
    result = sim.py_simulate(s, timepoints)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(len(species_ind)):
        plt.plot(timepoints, result.py_get_result()[:, species_ind[i]])
        plt.legend(SpeciesToPlot)
    plt.show()

