from modules.CreateSubsystem import *
from libsbml import *

class NewSubsystem(object):
    """ 
        Attributes:
            Subsystem : SBMLDocument object
            NewName : String type
            NewDocument : New SBMLDocument object to store the copy
    """
    def __init__(self, Subsystem):
        self.Subsystem = Subsystem

    def getSubsystem(self):
        """ Returns the SBMLDocument object """
        return self.Subsystem
    
    def setSubsystem(self, Subsystem):
        """ Set the SBMLDocument object """
        self.Subsystem = Subsystem

    def getNewName(self):
        """ Returns the new name of the subsystem """
        return self.NewName

    def setNewName(self, NewName):
        self.NewName = NewName

    def createNewSubsystem(self, NewName):
        """ Takes the name given and returns a copy of the subsystem
        given in the SBMLDocument object in the Subsystem attribute
        """
        NewDocument = createNewDocument(self.getLevel(),self.getVersion())
        modelOld = self.getSubsystem().getModel()
        check(modelOld, 'retreived old model')
        model = NewDocument.createModel()
        check(model, 'created new model in the new document')
        check(NewDocument.setModel(modelOld),'setting old model to new model')
        model = NewDocument.getModel()
        status = model.setId(model.getId() + NewName)
        check(status,'set id of the new model')
        check(model.setName(model.getName() + NewName), 'set new model name')
        for compartments in model.getListOfCompartments():
            oldid = compartments.getId()
            compartments.renameSIdRefs(oldid,oldid + NewName)
            model.addCompartment(compartments)
        # Setting species with new names
        for species in model.getListOfSpecies():
            oldid = species.getId()
            species.renameSIdRefs(oldid,oldid + NewName)
            model.addSpecies(species)
        for reactions in model.getListOfReactions():
            oldid = reactions.getId()
            reactions.renameSIdRefs(oldid,oldid + NewName)
            model.addReaction(reactions)
        for parameters in model.getListOfParameters():
            oldid = parameters.getId()
            parameters.renameSIdRefs(oldid,oldid + NewName)
            model.addParameter(parameters)
        return NewDocument