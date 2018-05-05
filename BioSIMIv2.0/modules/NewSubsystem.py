from libsbml import *
from modules.CreateSubsystem import *

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
        self.Subsystem =Subsystem

    def getNewName(self):
        """ Returns the new name of the subsystem """
        return self.NewName

    def setNewName(self, NewName):
        self.NewName = NewName

    def createNewSubsystem(self, NewName):
        """ Takes the name given and returns a copy of the subsystem
        given in the SBMLDocument object in the Subsystem attribute
        """
        model = self.getSubsystem().getModel()
        check(model, 'retreived old model')
        NewDocument = createNewDocument(model.getLevel(),model.getVersion())
        status = model.setId(model.getId() + NewName)
        check(status,'set id of the new model')

        # Rename all math formula. 
        for reaction in model.getListOfReactions():
            astnode = reaction.getKineticLaw().getMath()

            for parameter in model.getListOfParameters():
                oldid = parameter.getId()
                astnode.renameSIdRefs(oldid, oldid + NewName)
 
            for species in reaction.getListOfAllElements():
                if species.isSetId():
                    oldid = species.getId()
                    astnode.renameSIdRefs(oldid, oldid + NewName)
            reaction.getKineticLaw().setMath(astnode)

        # Rename all other IDs 
        elements = model.getListOfAllElements()
        # for parameter in model.getListOfParameters():
        for element in elements:
            # change the ID for the units. The units remain the same
            # the ids need to be updated. 
            try:
                if element.isSetUnits():
                    oldid = element.getUnits()
                    element.renameUnitSIdRefs(oldid, oldid + NewName)
            except:
                pass
            # Change the ids by appending the suffix given in NewName
            # if not element.isSetUnits():
            if element.isSetId():
                oldid = element.getId()
                newid = oldid + NewName
                element.renameSIdRefs(oldid,newid)
                element.setId(newid)
        model = elements[0].getModel()
        NewDocument.setModel(model)
        return NewDocument