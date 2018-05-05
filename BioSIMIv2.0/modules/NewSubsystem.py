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
        # model = NewDocument.createModel()
        # check(model, 'created new model in the new document')
        status = model.setId(model.getId() + NewName)
        check(status,'set id of the new model')
        # check(model.setName(model.getName() + NewName), 'set new model name')
        for reaction in model.getListOfReactions():
            astnode = reaction.getKineticLaw().getMath()

            for parameter in model.getListOfParameters():
                oldid = parameter.getId()
                astnode.renameSIdRefs(oldid, oldid + NewName)
 
            for species in reaction.getListOfAllElements():
                if species.isSetId():
                    oldid = species.getId()
                    astnode.renameSIdRefs(oldid, oldid + NewName)
                    # newFormula = formulaToL3String(astnode)
            reaction.getKineticLaw().setMath(astnode)

        elements = model.getListOfAllElements()
        newListOfElements = [] 
        for element in elements:
            if element.isSetId():
                oldid = element.getId()
                # print(oldid)
                newid = oldid + NewName
                element.renameSIdRefs(oldid,newid)
                element.setId(newid)
            # try:    
            #     if element.isSetUnits():
            #         oldid = element.getUnits()
            #         newid = oldid + NewName
            #         element.setUnits(newid)
            #         element.renameUnitSIdRefs(oldid,newid)
            # except:
            #     continue
            # if element.isSetName():
            #     oldid = element.getName()
            #     element.setName(oldid + NewName)
            newListOfElements.append(element)
        model = newListOfElements[0].getModel()
        NewDocument.setModel(model)
        return NewDocument