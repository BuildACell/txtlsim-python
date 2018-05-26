import libsbml 
from modules.SimpleModel import *
from modules.setIdFromNames import *

class Subsystem(object):

    def __init__(self, SubsystemDoc, System = None):
        self.SubsystemDoc = SubsystemDoc
        self.System = System
        
    def getSubsystemDoc(self):
        return self.SubsystemDoc

    def setSubsystemDoc(self, doc):
        self.SubsystemDoc = doc

    def setSystem(self,systemObj):
        self.System = systemObj

    def getSystem(self):
        return self.System

    def renameSName(self, old_name, new_name):
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving model from document in renameSName')
        mod_obj = SimpleModel(model)
        species = mod_obj.getSpeciesByName(old_name)
        if species == None:
            print('No species named' + old_name + 'found.')
            return
        check(species.setName(new_name), 'setting new name from rename function call')

    def convertSubsystemLevelAndVersion(self, newLevel, newVersion):
        document = self.getSubsystemDoc()
        check(document,'retreiving document object for subsystem in convert function')
        config = ConversionProperties()
        if config != None:
            config.addOption('setLevelAndVersion')
        # Now, need to set the target level and version (to which to convert the document)
        # Use the setTargetNamespaces() object of the ConversionsProperties as follows.
        # First, need to create a new SBMLNamespaces object with the desired (target) level and version
        sbmlns = SBMLNamespaces(newLevel,newVersion)
        check(sbmlns, 'creating new sbml namespaces')
        # check(config.setTargetNamespaces(sbmlns),'setting target namespaces')
        config.setTargetNamespaces(sbmlns)
        # Use the SBMLDocument.convert(ConversionsProperties) syntax to convert
        check(document.convert(config),'converting document level and version')
        conv_status = document.checkL3v1Compatibility()
        if conv_status != 0:
            print('SBML Level/Version conversion failed')
            return


    def renameSId(self, oldSId, newSId): 
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

        document = self.getSubsystemDoc()
        check(document,'retreiving document from subsystem in renameSId')
        element = document.getElementBySId(oldSId)

        if element == None:
            print("Found no element with SId '{0}' in subsystem {1}".format(oldSId,document.getModel().getId()))
            return
        
        # found element -> renaming
        check(element.setId(newSId),'setting new SId in renameSId')


        # update all references to this element
        allElements = document.getListOfAllElements()
        check(allElements,'getting list of all elements in renameSId')
        for i in range(allElements.getSize()):
            current = allElements.get(i)
            current.renameSIdRefs(oldSId, newSId)
        return document 

    def getAllIds(self):
        """ Returns all SIds in the document in string format
        """
        document = self.getSubsystemDoc()
        check(document,'retreiving document from subsystem in getAllIds')
        allElements = document.getListOfAllElements()
        result = []
        if (allElements == None or allElements.getSize() == 0):
            return result 
        for i in range (allElements.getSize()):
            current = allElements.get(i) 
            if (current.isSetId() and current.getTypeCode() != libsbml.SBML_EVENT and current.getTypeCode() != libsbml.SBML_LOCAL_PARAMETER):
                result.append(current.getId()) 
        return result     
    
    def suffixAllElementIds(self, name):
        """ The given name attribute is suffixed to all components
         of self (the subsystem object).
        """
        document = self.getSubsystemDoc()
        check(document,'retreiving document from subsystem in suffixAllElements')
        allids = self.getAllIds()
        for oldid in allids:
            if document.getElementBySId(oldid) != None:
                self.renameSId(oldid, oldid + '_' + name)

        ## Use if want to rename all names too
        # elements = document.getListOfAllElements()
        # for element in elements:
        #     if element.isSetName():
        #         oldname = element.getName()
        #         newname = oldname + '_' + name
        #         element.setName(newname)

        return document

    def setCompartments(self, newCompartments):
        document = self.getSubsystemDoc()
        check(document,'retreiving document from subsystem in setSubsystemCompartments')
        compartments = document.getModel().getListOfCompartments()
        check(compartments,'retreiving list of compartments in setSubsystemCompartments')
        if len(compartments) != len(newCompartments):
            print('Warning : - The number of compartments given is not the same as the number of compartments in the model.') 
            for i in range(len(newCompartments)):
                # rename compartment name and id
                if compartments.get(i).isSetName():
                    status = compartments.get(i).setName(newCompartments[i])
                    check(status, 'setting name of compartment in setSubsystemCompartment')
                oldid = compartments.get(i).getId()
                check(oldid,'retreiving oldid in setSubsystemCompartments')
                self.renameSId(oldid,newCompartments[i])   
   
        else:
            for i in range(len(compartments)):
                # rename compartment name and id
                if compartments.get(i).isSetName():
                    status = compartments.get(i).setName(newCompartments[i])
                    check(status, 'setting name of compartment in setSubsystemCompartments')
                oldid = compartments.get(i).getId()
                check(oldid,'retreiving oldid in setSubsystemCompartments')
                self.renameSId(oldid,newCompartments[i])   
   
    def createNewModel(self, modelId, timeUnits, extentUnits, substanceUnits):
        model = self.getSubsystemDoc().createModel()
        if model == None:
            print('Unable to create Model object.')
            sys.exit(1)
        status = model.setId(modelId)
        if status != LIBSBML_OPERATION_SUCCESS:
            print('Unable to set identifier on the Model object')
            sys.exit(1)
        check(model.setTimeUnits(timeUnits), 'set model-wide time units')
        check(model.setExtentUnits(extentUnits), 'set model units of extent')
        check(model.setSubstanceUnits(substanceUnits),
              'set model substance units')
        return model

    def mergeSubsystemModels(self, ListOfSubsystems):
    # functions, units, compartments, species, parameters, 
    # initial assignments, rules, constraints, reactions, and events
        document = self.getSubsystemDoc()
        check(document,'retreiving document in mergeSubsystem')
        model_base = ListOfSubsystems[0].getSubsystemDoc().getModel()
        check(model_base,'retreiving model in mergeSubsystems')
        model = self.createNewModel('merged_model',model_base.getTimeUnits(), model_base.getExtentUnits(), model_base.getSubstanceUnits())
        check(document.setModel(model),'setting model for document in mergeSubsystem')
        for subsystem in ListOfSubsystems:
            mod = subsystem.getSubsystemDoc().getModel()
            check(mod,'retreiving model in mergeSubsystem')
            if mod.getNumCompartmentTypes() != 0:
                for each_compartmentType in mod.getListOfCompartmentType():
                    model.addCompartment(each_compartmentType)
            if mod.getNumConstraints() != 0:
                for each_constraint in mod.getListOfConstraints():
                    model.addConstraint(each_constraint)
            if mod.getNumInitialAssignments() != 0:
                for each_initialAssignment in mod.getListOfInitialAssignments():
                    model.addInitialAssignment(each_initialAssignment)
            if mod.getNumFunctionDefinitions() != 0:
                for each_functionDefinition in mod.getListOfFunctionDefinitions():
                    model.addFunctionDefinition(each_functionDefinition)
            if mod.getNumRules() != 0:
                for each_rule in mod.getListOfRules():
                    model.addRule(each_rule)
            if mod.getNumEvents() != 0:
                for each_event in mod.getListOfEvents():
                    model.addEvent(each_event)
            if mod.getNumCompartments() != 0:
                for each_compartment in mod.getListOfCompartments():
                    model.addCompartment(each_compartment)
            if mod.getNumParameters() != 0:
                for each_parameter in mod.getListOfParameters():
                    model.addParameter(each_parameter)
            if mod.getNumUnitDefinitions() != 0:
                for each_unit in mod.getListOfUnitDefinitions():
                    model.addUnitDefinition(each_unit)
            if mod.getNumReactions() != 0:
                for each_reaction in mod.getListOfReactions():
                    model.addReaction(each_reaction)
            model.setAreaUnits(mod.getAreaUnits())
            model.setExtentUnits(mod.getExtentUnits())
            model.setLengthUnits(mod.getLengthUnits())
            model.setSubstanceUnits(mod.getSubstanceUnits())
            model.setTimeUnits(mod.getTimeUnits())
            model.setVolumeUnits(mod.getVolumeUnits())

   
    def shareSubsystems(self, ListOfSubsystems, ListOfSharedResources):
        self.mergeSubsystemModels(ListOfSubsystems)
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving model in shareSubsystems')
        model_obj = SimpleModel(model)
        final_species_hash_map = {}
        mod_id = ''
        for subsystem in ListOfSubsystems:
            mod = subsystem.getSubsystemDoc().getModel()
            check(mod,'retreiving subsystem model in shareSubsystems')
            mod_id += '_' + mod.getId()
            if not ListOfSharedResources:
                species_list = mod.getListOfSpecies()
                check(species_list,'retreiving list of species of susbsytem model in shareSubsystems')
                for species in species_list:
                    check(model.getListOfSpecies().append(species),'appending list of species when ListOfSharedResources is empty, in shareSubsystems')
            else:
                # Set the list of reactions in the final subsystem. Get the list of
                # reactions in the input subsystem and set it to final subsystem
                species_hash_map = {}
                for species in mod.getListOfSpecies():
                    species_name = species.getName()
                    check(species_name,'getting species name in shareSubsystems')
                    if species_name in ListOfSharedResources:
                    # Maintain the dictionary for all species in the input subsystems by their name
                        species_hash_map[species_name] = species
                    else:
                        check(model.getListOfSpecies().append(species),'appending species to list of species in model in shareSubsystems')
                for species_name in species_hash_map:
                    if final_species_hash_map.get(species_name):
                        #If the final hash map already has that species then append to
                        # the same instead of duplicating
                        final_species_hash_map[species_name].append(
                            species_hash_map[species_name])
                    else:
                        # For all the species in the dictionary not already in the final
                        # hash map, save them to the final hash map dictionary.
                        final_species_hash_map[species_name] = [
                            species_hash_map[species_name]]

        for unique_species_name in final_species_hash_map:
            cumulative_amount = 0
            if len(final_species_hash_map[unique_species_name]) > 1: 
                uni_sp = final_species_hash_map[unique_species_name][0]
                    # For any species with same name 
                    # which were present in more than one subsystem
                count = 0
                for i in final_species_hash_map[unique_species_name]:
                    cumulative_amount += i.getInitialAmount()
                    check(model.getListOfSpecies().append(i),'appending species to list of species in model in shareSubsystems')
                    oldid = i.getId()
                    check(oldid,'getting olid in shareSubsystems')
                    newid = i.getName() + '_shared'
                    self.renameSId(oldid, newid)
                    if count >= 1:
                        check(model.getListOfSpecies().remove(newid),'removing from list of species in shareSubsystems')
                    count += 1
                sp = model_obj.getSpeciesByName(uni_sp.getName())
                # if type(sp) is list: 
                    # for sp_i in sp:
                        # check(sp_i.setInitialAmount(cumulative_amount),'setting initial amount to cumulative in shareSubsystems')
                # else:
                    # check(sp.setInitialAmount(cumulative_amount),'setting initial amount to cumulative in shareSubsystems')
            else:
                # If there are no species with multiple occurence in different subsystems
                # then just add the list of all species maintained in the final hash map
                # to our new subsystem's list of species.
                check(model.getListOfSpecies().append(final_species_hash_map[unique_species_name][0]),'appending to list of species in shareSubsystems')
                # model.getListOfSpecies().append(final_species_hash_map[unique_species_name][0])
        
        # Updating model id
        check(model.setId('shared_Subsystems_' + mod_id),'setting new model id for shared model')


    def combineSubsystems(self, ListOfSubsystems, combineNames):
        ListOfResources = self.getSystem().ListOfSharedResources
        self.shareSubsystems(ListOfSubsystems,ListOfResources)
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving self model in combineSubsystems')
        model_obj = SimpleModel(model)
        mod_id = ''

        for subsystem in ListOfSubsystems:
            mod = subsystem.getSubsystemDoc().getModel()
            check(mod,'retreiving subsystem model in combineSubsystems')
            mod_id += '_' + mod.getId()
            if combineNames == False:
                if mod.getNumSpecies() != 0:
                  for each_species in mod.getListOfSpecies():
                        if each_species.getName() not in ListOfResources:
                            model.addSpecies(each_species)

        # The final species hash map is a dictionary for all the species that will be
        # in the final subsystem.
        if combineNames == True:
            final_species_hash_map = {}
            for subsystem in ListOfSubsystems:
                mod_id += '_' + mod.getId()
                # Set the list of reactions in the final subsystem. Get the list of
                # reactions in the input subsystem and set it to final subsystem
                species_hash_map = {}
                for species in subsystem.getSubsystemDoc().getModel().getListOfSpecies():
                    if species.getName() not in ListOfResources:
                    # Maintain the dictionary for all species in the input subsystems by their name
                        species_hash_map[species.getName()] = species
                for species_name in species_hash_map:
                    if final_species_hash_map.get(species_name):
                        #If the final hash map already has that species then append to
                        # the same instead of duplicating
                        final_species_hash_map[species_name].append(
                            species_hash_map[species_name])
                    else:
                        # For all the species in the dictionary not already in the final
                        # hash map, save them to the final hash map dictionary.
                        final_species_hash_map[species_name] = [
                            species_hash_map[species_name]]

            for unique_species_name in final_species_hash_map:
                cumulative_amount = 0
                if len(final_species_hash_map[unique_species_name]) > 1: 
                    uni_sp = final_species_hash_map[unique_species_name][0]
                        # For any species with same name 
                        # which were present in more than one subsystem
                    count = 0
                    for i in final_species_hash_map[unique_species_name]:
                        cumulative_amount += i.getInitialAmount()
                        model.addSpecies(i)
                        oldid = i.getId()
                        check(oldid, 'retreiving oldid combineSubsystems')
                        allids = self.getAllIds()
                        trans = SetIdFromNames(allids)
                        newid = trans.getValidIdForName(i.getName()) + '_combined'
                        self.renameSId(oldid, newid)
                        if count >= 1:
                            check(model.removeSpecies(newid),'removing species in combineSubsystems')
                        count += 1
                    sp = model_obj.getSpeciesByName(uni_sp.getName())
                    # if type(sp) is list: 
                        # for sp_i in sp:
                            # check(sp_i.setInitialAmount(cumulative_amount),'setting initial amount to cumulative in combineSubsystems')
                    # else:
                        # check(sp.setInitialAmount(cumulative_amount),'setting initial amount to cumulative in combineSubsystems')
                else:
                    # If there are no species with multiple occurence in different subsystems
                    # then just add the list of all species maintained in the final hash map
                    # to our new subsystem's list of species.
                    model.addSpecies(final_species_hash_map[unique_species_name][0])
                    # check(model.addSpecies(final_species_hash_map[unique_species_name][0]),'adding species in combineSubsystems')
      
       # Updating model id
        check(model.setId('combined_Subsystems_' + mod_id),'setting new model id for shared model')

  
    def connectSubsystems(self, ListOfSubsystems, combineNames, connectionLogic, inputSpecies = None):
        self.combineSubsystems(ListOfSubsystems, combineNames)
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving self model in connectSubsystem')
        # The connection logic given by user species two or more different species
        # but that are bound to each other.
        # Set the initial amount of the input in the output subsystem to zero since it's not
        # isolated anymore.
        model_obj = SimpleModel(model)
        if inputSpecies:
            if type(inputSpecies) is list:
                for inp_sp in inputSpecies:
                    check(model_obj.getSpeciesByName(inp_sp).setInitialAmount(0.0),'setting initial amount to 0 in connectSubsystem')
            else:
                check(model_obj.getSpeciesByName(inputSpecies).setInitialAmount(0.0),'setting initial amount to 0 in connectSubsystem')
        for species_name in connectionLogic.keys():
            # Get the ids of the concerned species from the
            # connection logic given by the user
            x = model_obj.getSpeciesByName(species_name)
            y = model_obj.getSpeciesByName(connectionLogic[species_name])
            if type(x) is list or type(y) is list:
                print('Error : Multiple species exist in the model which have the same name to what is given in the connection map. Make sure that connecting species are unique. Use the renameSName function to rename the species before trying to connect')
                return

            if x.getCompartment() == y.getCompartment():
                s = sum([x.getInitialAmount(), y.getInitialAmount()])
                # x and y should also have the same id so that they go into reactions as one.
                # Also, set the initial amount of the species to be equal to the
                # sum of their individual amounts
                check(x.setInitialAmount(s),'setting initial amount of x in connectSubsystem')
                check(y.setInitialAmount(s),'setting initial amount of y in connectSubsystem')
                # Rename ID of x by that of y
                oldid = x.getId()
                check(oldid,'retreiving oldid of x in connectSubsystem')
                newid = y.getId()
                check(newid,'retreiving newid of y in connectSubsystem')
                self.renameSId(oldid, newid)
                # Remove x from species list to avoid duplication
                id_to_remove = model_obj.getSpeciesByName(x.getName()).getId()
                model.getListOfSpecies().remove(id_to_remove)