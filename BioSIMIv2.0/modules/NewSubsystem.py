from libsbml import *
import libsbml

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
        
    def renameSId (self, oldSId, newSId): 
        # 
        # @file    renameSId.py
        # @brief   Utility program, renaming a specific SId 
        #          while updating all references to it.
        # @author  Frank T. Bergmann
        # 
        # <!--------------------------------------------------------------------------
        # This sample program is distributed under a different license than the rest
        # of libSBML.  This program uses the open-source MIT license, as follows:
        # 
        # Copyright (c) 2013-2018 by the California Institute of Technology
        # (California, USA), the European Bioinformatics Institute (EMBL-EBI, UK)
        # and the University of Heidelberg (Germany), with support from the National
        # Institutes of Health (USA) under grant R01GM070923.  All rights reserved.
        # 
        # Permission is hereby granted, free of charge, to any person obtaining a
        # copy of this software and associated documentation files (the "Software"),
        # to deal in the Software without restriction, including without limitation
        # the rights to use, copy, modify, merge, publish, distribute, sublicense,
        # and/or sell copies of the Software, and to permit persons to whom the
        # Software is furnished to do so, subject to the following conditions:
        # 
        # The above copyright notice and this permission notice shall be included in
        # all copies or substantial portions of the Software.
        # 
        # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
        # THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
        # DEALINGS IN THE SOFTWARE.
        # 
        # Neither the name of the California Institute of Technology (Caltech), nor
        # of the European Bioinformatics Institute (EMBL-EBI), nor of the University
        # of Heidelberg, nor the names of any contributors, may be used to endorse
        # or promote products derived from this software without specific prior
        # written permission.
        # ------------------------------------------------------------------------ -->
        # 

        if oldSId == newSId:
            print("The Ids are identical, renaming stopped.")
            return

        if not libsbml.SyntaxChecker.isValidInternalSId(newSId):
            print("The new SId '{0}' does not represent a valid SId.".format(newSId))
            return

        document = self.getSubsystem()
        # find elements for old id
        element = document.getElementBySId(oldSId)
        if element == None:
            print("Found no element with SId '{0}'".format(oldSId))
            return
        
        # found element -> renaming
        element.setId(newSId)

        # update all references to this element
        allElements = document.getListOfAllElements()
        for i in range(allElements.getSize()):
            allElements.get(i).renameSIdRefs(oldSId, newSId)
        
        return document 

    def getAllIds(self):
        """ Returns all SIds in the document in string format
        """
        document = self.getSubsystem()
        allElements = document.getListOfAllElements()
        result = []
        if (allElements == None or allElements.getSize() == 0):
            return result 
    
        for i in range (0, allElements.getSize()):
            current = allElements.get(i) 
            if (current.isSetId() and current.getTypeCode() != libsbml.SBML_LOCAL_PARAMETER):
                result.append(current.getId()) 
        return result     

    def createNewSubsystem(self, NewName):
        """ Takes the name given and returns a copy of the subsystem
        given in the SBMLDocument object in the Subsystem attribute
        """
        document = self.getSubsystem()
        allids = self.getAllIds()
        for oldid in allids:
            self.renameSId(oldid,oldid + NewName)
        
        # Rename all names too
        elements = document.getListOfAllElements()
        for element in elements:
            if element.isSetName():
                oldname = element.getName()
                newname = oldname + NewName
                element.setName(newname)
        return document