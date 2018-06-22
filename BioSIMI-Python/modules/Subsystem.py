import libsbml 
import time
from modules.NewReaction import *
from modules.setIdFromNames import *
from modules.utilityFunctions import *

class Subsystem(object):

    def __init__(self, SubsystemDoc, System = None):
        self.SubsystemDoc = SubsystemDoc
        self.System = System
        
    def getSubsystemDoc(self):
        '''
        Returns the SBMLDocument object of the Subsystem
        '''
        return self.SubsystemDoc

    def setSubsystemDoc(self, doc):
        '''
        The sbmlDoc is set as the SBMLDocument of the Subsystem
        '''
        self.SubsystemDoc = doc

    def setSystem(self,systemObj):
        '''
        The systemObject is set as the System for the Subsystem
        '''
        self.System = systemObj

    def getSystem(self):
        '''
        Returns the System object in which the Subsystem is placed.
        '''
        return self.System

    def renameSName(self, old_name, new_name):
        '''
        Search the SBMLDocument for the oldName and rename all such 
        components by the newName
        '''
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving model from document in renameSName')
        mod_obj = SimpleModel(model)
        species = mod_obj.getSpeciesByName(old_name)
        if species == None:
            print('No species named' + old_name + 'found.')
            return
        if type(species) is list:
            for sp in species:
                check(sp.setName(new_name), 'setting the new name from rename to the list of species')
        else:
            check(species.setName(new_name), 'setting new name from rename function call')

    def convertSubsystemLevelAndVersion(self, newLevel, newVersion):
        '''
        Converts the SBMLDocument of the current Subsytem to the newLevel and newVersion
        '''
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
        """ 
        Returns all SIds in the document in string format
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
        '''
        All elements identifiers in the
        SBMLDocument of the Subsystem are suffixed with name
        '''
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
        '''
    	The newCompartments list is set as the new ListOfCompartments 
        in theSBMLDocument of the Subsystem
        '''
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
        '''
        Creates a new Model object in the SBMLDocument of the Subsystem 
        with the given attributes
        '''
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
        '''
        The ListOfSubsystems are merged together. All components are 
        merged together except the Species.
        '''
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
            # Obsolete in SBML Level 3 
            # if mod.getNumCompartmentTypes() != 0:
            #     for each_compartmentType in mod.getListOfCompartmentType():
            #         model.addCompartmentType(each_compartmentType)
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

   
    def shareSubsystems(self, ListOfSubsystems, ListOfSharedResources, mode = 'volume', combineCall = False):
        '''
        The ListOfSubsystems are merged and all Species are also added to the 
        Subsystem object. The Species in ListOfSharedResources are combined together 
        and so are shared by all Subsystems in the ListOfSubsystems. The Model id is also updated.
        '''
        self.mergeSubsystemModels(ListOfSubsystems)
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving model in shareSubsystems')
        model_obj = SimpleModel(model)
        mod_id = ''
        total_size = 0
        if combineCall == False:
            total_size = self.getSystem().Size
        else:
            for subsystem in ListOfSubsystems:
                total_size += subsystem.getSubsystemDoc().getModel().getCompartment(0).getSize()

        check(model.getCompartment(0).setSize(total_size), 'setting compartment size in model')
        final_species_hash_map = {}
        if mode == 'volume':
            for subsystem in ListOfSubsystems:
                mod = subsystem.getSubsystemDoc().getModel()
                check(mod,'retreiving subsystem model in shareSubsystems')
                mod_id += '_' + mod.getId()
                # if list of shared resources is empty
                if not ListOfSharedResources:
                    species_list = mod.getListOfSpecies()
                    check(species_list,'retreiving list of species of susbsytem model in shareSubsystems')
                    for species in species_list:
                        ssys_size = 0
                        cumulative_amount = 0
                        species_amount = 0
                        ssys_size = species.getModel().getCompartment(0).getSize()
                        cumulative_amount = (species.getInitialAmount())*ssys_size
                        species_amount = cumulative_amount/total_size
                        check(model.addSpecies(species),'adding species to the model when ListOfSharedResources is empty, in shareSubsystems')
                        check(model.getSpecies(species.getId()).setInitialAmount(species_amount),'setting initial amount to cumulative in shareSubsystems')
                else:
                    # Set the list of reactions in the final subsystem. Get the list of
                    # reactions in the input subsystem and set it to final subsystem
                    species_hash_map = {}
                    for species in mod.getListOfSpecies():
                        ssys_size = 0
                        cumulative_amount = 0
                        species_amount = 0
                        species_name = species.getName()
                        check(species_name,'getting species name in shareSubsystems')
                        if species_name in ListOfSharedResources:
                        # Maintain the dictionary for all species in the input subsystems by their name
                            species_hash_map[species_name] = species
                        else:
                            ssys_size = species.getModel().getCompartment(0).getSize()
                            cumulative_amount = (species.getInitialAmount())*ssys_size
                            species_amount = cumulative_amount/total_size
                            check(model.addSpecies(species),'adding species to the model in shareSubsystems')
                            check(model.getSpecies(species.getId()).setInitialAmount(species_amount),'setting initial amount in shareSubsystems')
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

            allids = self.getAllIds()
            trans = SetIdFromNames(allids)
            for unique_species_name in final_species_hash_map:
                ssys_size = 0
                cumulative_amount = 0
                species_amount = 0
                if len(final_species_hash_map[unique_species_name]) > 1: 
                    uni_sp = final_species_hash_map[unique_species_name][0]
                        # For any species with same name 
                        # which were present in more than one subsystem
                    count = 0
                    for i in final_species_hash_map[unique_species_name]:
                        ssys_size = i.getModel().getCompartment(0).getSize()
                        cumulative_amount += (i.getInitialAmount())*ssys_size
                        species_amount = cumulative_amount/total_size
                        check(model.addSpecies(i),'add species to model in shareSubsystems')
                        oldid = i.getId()
                        check(oldid,'getting olid in shareSubsystems')
                        newid = trans.getValidIdForName(i.getName()) + '_shared'
                        self.renameSId(oldid, newid)
                        if count >= 1:
                            check(model.removeSpecies(newid),'removing species from the model in shareSubsystems')
                        count += 1
                    sp = model_obj.getSpeciesByName(uni_sp.getName())
                    if type(sp) is list: 
                        for sp_i in sp:
                            check(sp_i.setInitialAmount(species_amount),'setting initial amount to cumulative in shareSubsystems')
                    else:
                        check(sp.setInitialAmount(species_amount),'setting initial amount to cumulative in shareSubsystems')
                else:
                #     # If there are no species with multiple occurence in different subsystems
                #     # then just add the list of all species maintained in the final hash map
                #     # to our new subsystem's list of species.
                    i = final_species_hash_map[unique_species_name][0]
                #     ssys_size = i.getModel().getCompartment(0).getSize()
                #     cumulative_amount = (i.getInitialAmount())*ssys_size
                #     species_amount = cumulative_amount/total_size
                    check(model.addSpecies(i),'adding species to the model in shareSubsystems')
                #     check(i.setInitialAmount(species_amount),'setting initial amount of species in shareSubsystems')
        elif mode == 'virtual':
            for subsystem in ListOfSubsystems:
                mod = subsystem.getSubsystemDoc().getModel()
                check(mod,'retreiving subsystem model in shareSubsystems')
                mod_id += '_' + mod.getId()
                if not ListOfSharedResources:
                    species_list = mod.getListOfSpecies()
                    check(species_list,'retreiving list of species of susbsytem model in shareSubsystems')
                    for species in species_list:
                        check(model.addSpecies(species),'adding species to the model when ListOfSharedResources is empty, in shareSubsystems')
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
                            check(model.addSpecies(species),'adding species to the model in shareSubsystems')
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

            allids = self.getAllIds()
            trans = SetIdFromNames(allids)
            for unique_species_name in final_species_hash_map:
                cumulative_amount = 0
                if len(final_species_hash_map[unique_species_name]) > 1: 
                        # For any species with same name 
                        # which were present in more than one subsystem
                    count = 0
                    for i in final_species_hash_map[unique_species_name]:
                        check(model.addSpecies(i),'add species to model in shareSubsystems')
                        oldid = i.getId()
                        check(oldid,'getting olid in shareSubsystems')
                        newid = trans.getValidIdForName(i.getName()) + '_shared'
                        self.renameSId(oldid, newid)
                        if count >= 1:
                            check(model.removeSpecies(newid),'removing species from the model in shareSubsystems')
                        count += 1
               # else:
                #     # If there are no species with multiple occurence in different subsystems
                #     # then just add the list of all species maintained in the final hash map
                #     # to our new subsystem's list of species.
                #     i = final_species_hash_map[unique_species_name][0]
                #     ssys_size = i.getModel().getCompartment(0).getSize()
                #     cumulative_amount = (i.getInitialAmount())*ssys_size
                #     species_amount = cumulative_amount/total_size
                #     check(model.addSpecies(i),'adding species to the model in shareSubsystems')
                #     check(i.setInitialAmount(species_amount),'setting initial amount of species in shareSubsystems')
 

        # Updating model id
        check(model.setId('shared_Subsystems_' + mod_id),'setting new model id for shared model')


    def combineSubsystems(self, ListOfSubsystems, combineNames, mode = 'volume'):
        '''
        The ListOfSubsystems are combined together by adding all Species and combining 
	    Species with the same name together if combineNames is True. 
        The ListOfSharedResources of the System in which the Subsystem is placed 
        is used to share the Species in the list. Other Species are combined depending on 
        the combineNames (True or False)
        '''
        for subsystem in ListOfSubsystems:
            if subsystem.getSystem() != ListOfSubsystems[0].getSystem():
                print('BioSIMI-Python ERROR -- The Subsystems being combined are not in the same System')
                return

        ListOfResources = ListOfSubsystems[0].getSystem().ListOfSharedResources
        self.shareSubsystems(ListOfSubsystems,ListOfResources, mode, True)
        writeSBML(self.getSubsystemDoc(),'models/DP_IFFL_shared2.xml')
        model = self.getSubsystemDoc().getModel()
        check(model,'retreiving model in combineSubsystems')
        simpleModel = SimpleModel(model)
        mod_id = ''

        if mode == 'volume':
            if combineNames == False:
                total_size = 0
                for subsystem in ListOfSubsystems:
                    sub_model = subsystem.getSubsystemDoc().getModel()
                    # check(mod,'retreiving subsystem model in combineSubsystems')
                    mod_id += '_' + sub_model.getId()
                    total_size += sub_model.getCompartment(0).getSize()
                    # if mod.getNumSpecies() != 0:
                        # for each_species in mod.getListOfSpecies():
            #                 if each_species.getName() not in ListOfResources:
            #                     # ssys_size = each_species.getModel().getCompartment(0).getSize()
            #                     # cumulative_amount = (each_species.getInitialAmount())*ssys_size
            #                     # species_amount = cumulative_amount/total_size
            #                     # check(each_species.setInitialAmount(species_amount),'setting initial amount to cumulative in combineSubsystems False')
            #                     model.addSpecies(each_species)

            # The final species hash map is a dictionary for all the species that will be
            # in the final subsystem.
            if combineNames == True:
                final_species_hash_map = {}
                final_reaction_map = {}
                total_size = 0
                # final_parameter_map = {}
                for subsystem in ListOfSubsystems:
                    sub_model = subsystem.getSubsystemDoc().getModel()
                    total_size += sub_model.getCompartment(0).getSize()
                    mod_id += '_' + sub_model.getId()
                    # Finding duplicate species by name
                    species_hash_map = {}
                    for species in sub_model.getListOfSpecies():
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

                    # Finding duplicate reactions by the reaction string
                    reaction_map = {}
                    for reaction in sub_model.getListOfReactions():
                        rc1_list = reaction.getListOfReactants()
                        pt1_list = reaction.getListOfProducts()
                        rStr = ''
                        for i in range(len(rc1_list)):
                            sref = rc1_list[i]
                            rStr += sub_model.getElementBySId(sref.getSpecies()).getName()
                            if i < (len(rc1_list) - 1):
                                rStr += ' + '
                        if reaction.getReversible():
                            rStr += ' <-> '
                        else:
                            rStr += ' --> '
                        for i in range(len(pt1_list)):
                            sref = pt1_list[i]
                            rStr += sub_model.getElementBySId(sref.getSpecies()).getName()
                            if i < (len(pt1_list) - 1):
                                rStr += ' + '

                        reaction_map[rStr] = reaction

                    for rStr in reaction_map:
                        if final_reaction_map.get(rStr):
                            final_reaction_map[rStr].append(reaction_map[rStr])
                        else:
                            final_reaction_map[rStr] = [reaction_map[rStr]]
                
                    # Finding duplicate parameters by name and value
                    # parameter_map = {}
                    # for param in sub_model.getListOfParameters():
                    #     parameter_map[param.getName()] = param
                    # for param_name in parameter_map:
                    #     if final_parameter_map.get(param_name):
                    #         final_parameter_map[param_name].append(parameter_map[param_name])
                    #     else:
                    #         final_parameter_map[param_name] = [parameter_map[param_name]]

                # Removing duplicate global parameters and adding only one
                # for param_name in final_parameter_map:
                #     if len(final_parameter_map[param_name]) > 1:
                #         # uni_param = final_parameter_map[param_name][0]
                #         for ind in range(0,len(final_parameter_map[param_name])):
                #             i = final_parameter_map[param_name][ind]
                #             if ind > 0:
                #                 model.removeParameter(i.getId())
                #         # model.addParameter(uni_param)
                #         print('BioSIMI-Python WARNING -- Removing all duplicates of global parameter {0} in the combined model. Check the value to ensure model is consistent.'.format(param_name))
                        
                # Removing duplicate reactions and adding only one
                for rxn_str in final_reaction_map:
                    if len(final_reaction_map[rxn_str]) > 1:
                        for ind in range(0,len(final_reaction_map[rxn_str])):
                            i = final_reaction_map[rxn_str][ind]
                            if ind > 0:
                                status = model.removeReaction(i.getId())
                                if status != None:
                                    print('BioSIMI-Python WARNING -- Removing all duplicates of the reaction {0} in the combined model. Check the reaction rate to ensure model is consistent.'.format(rxn_str))

                # Removing duplicate species 
                for unique_species_name in final_species_hash_map:
                    cumulative_amount = 0
                    if len(final_species_hash_map[unique_species_name]) > 1: 
                        uni_sp = final_species_hash_map[unique_species_name][0]
                            # For any species with same name 
                            # which were present in more than one subsystem
                        count = 0
                        for i in final_species_hash_map[unique_species_name]:
                            # ssys_size = i.getModel().getCompartment(0).getSize()
                            # cumulative_amount += (i.getInitialAmount())*ssys_size
                            cumulative_amount += (model.getSpecies(i.getId()).getInitialAmount())
                            oldid = i.getId()
                            check(oldid, 'retreiving oldid combineSubsystems')
                            allids = self.getAllIds()
                            trans = SetIdFromNames(allids)
                            newid = trans.getValidIdForName(i.getName()) + '_combined'
                            self.renameSId(oldid, newid)
                            if count >= 1:
                                check(model.removeSpecies(newid),'removing species in combineSubsystems')
                            count += 1

                        # species_amount = cumulative_amount/total_size
                        species_amount = cumulative_amount
                        # check(model.addSpecies(uni_sp), 'adding species to the model in combineSubsystems')
                        sp = simpleModel.getSpeciesByName(uni_sp.getName())
                        if type(sp) is list: 
                            for sp_i in sp:
                                check(sp_i.setInitialAmount(species_amount),'setting initial amount to cumulative in combineSubsystems')
                        else:
                            check(sp.setInitialAmount(species_amount),'setting initial amount to cumulative in combineSubsystems')
                    # else:
                        # If there are no species with multiple occurence in different subsystems
                        # then just add the list of all species maintained in the final hash map
                        # to our new subsystem's list of species.
                        # i = final_species_hash_map[unique_species_name][0]
                        # ssys_size = i.getModel().getCompartment(0).getSize()
                        # cumulative_amount = (i.getInitialAmount())*ssys_size
                        # species_amount = cumulative_amount/total_size
                        # check(i.setInitialAmount(species_amount),'setting initial amount to cumulative in combineSubsystems')
                        # model.addSpecies(i)
                        # check(model.addSpecies(final_species_hash_map[unique_species_name][0]),'adding species in combineSubsystems')
        
            check(model.getCompartment(0).setSize(total_size), 'setting compartment size in model')
        elif mode == 'virtual':
            if combineNames == False:
                total_size = 0
                for subsystem in ListOfSubsystems:
                    mod = subsystem.getSubsystemDoc().getModel()
                    total_size += mod.getCompartment(0).getSize()
                    check(mod,'retreiving subsystem model in combineSubsystems')
                    mod_id += '_' + mod.getId()
                    # if mod.getNumSpecies() != 0:
                    #     for each_species in mod.getListOfSpecies():
                    #         if each_species.getName() not in ListOfResources:
                    #             model.addSpecies(each_species)

            # The final species hash map is a dictionary for all the species that will be
            # in the final subsystem.
            if combineNames == True:
                final_species_hash_map = {}
                final_reaction_map = {}
                final_parameter_map = {}
                total_size = 0
                for subsystem in ListOfSubsystems:
                    sub_model = subsystem.getSubsystemDoc().getModel()
                    total_size += sub_model.getCompartment(0).getSize()
                    mod_id += '_' + sub_model.getId()
                    # Finding duplicate species by name
                    species_hash_map = {}
                    for species in sub_model.getListOfSpecies():
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

                    # Finding duplicate reactions by the reaction string
                    reaction_map = {}
                    for reaction in sub_model.getListOfReactions():
                        rc1_list = reaction.getListOfReactants()
                        pt1_list = reaction.getListOfProducts()
                        rStr = ''
                        for i in range(len(rc1_list)):
                            sref = rc1_list[i]
                            rStr += sub_model.getElementBySId(sref.getSpecies()).getName()
                            if i < (len(rc1_list) - 1):
                                rStr += ' + '
                        if reaction.getReversible():
                            rStr += ' <-> '
                        else:
                            rStr += ' --> '
                        for i in range(len(pt1_list)):
                            sref = pt1_list[i]
                            rStr += sub_model.getElementBySId(sref.getSpecies()).getName()
                            if i < (len(pt1_list) - 1):
                                rStr += ' + '

                        reaction_map[rStr] = reaction

                    for rStr in reaction_map:
                        if final_reaction_map.get(rStr):
                            final_reaction_map[rStr].append(reaction_map[rStr])
                        else:
                            final_reaction_map[rStr] = [reaction_map[rStr]]
                
                    # Finding duplicate parameters by name and value
                    parameter_map = {}
                    for param in sub_model.getListOfParameters():
                        parameter_map[param.getName()] = param
                    for param_name in parameter_map:
                        if final_parameter_map.get(param_name):
                            final_parameter_map[param_name].append(parameter_map[param_name])
                        else:
                            final_parameter_map[param_name] = [parameter_map[param_name]]

                # Removing duplicate global parameters and adding only one
                # for param_name in final_parameter_map:
                #     if len(final_parameter_map[param_name]) > 1:
                #         # uni_param = final_parameter_map[param_name][0]
                #         for ind in range(0,len(final_parameter_map[param_name])):
                #             i = final_parameter_map[param_name][ind]
                #             if ind > 0:
                #                 model.removeParameter(i.getId())
                #         # model.addParameter(uni_param)
                #         print('BioSIMI-Python WARNING -- Removing all duplicates of global parameter {0} in the combined model. Check the value to ensure model is consistent.'.format(param_name))
                        
                # Removing duplicate reactions and adding only one
                for rxn_str in final_reaction_map:
                    if len(final_reaction_map[rxn_str]) > 1:
                        for ind in range(0,len(final_reaction_map[rxn_str])):
                            i = final_reaction_map[rxn_str][ind]
                            if ind > 0:
                                status = model.removeReaction(i.getId())
                                if status != None:
                                    print('BioSIMI-Python WARNING -- Removing all duplicates of the reaction {0} in the combined model. Check the reaction rate to ensure model is consistent.'.format(rxn_str))

                # Removing duplicate species and adding only one
                for unique_species_name in final_species_hash_map:
                    if len(final_species_hash_map[unique_species_name]) > 1: 
                            # For any species with same name 
                            # which were present in more than one subsystem
                        count = 0
                        for i in final_species_hash_map[unique_species_name]:
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
                    else:
                        # If there are no species with multiple occurence in different subsystems
                        # then just add the list of all species maintained in the final hash map
                        # to our new subsystem's list of species.
                        model.addSpecies(final_species_hash_map[unique_species_name][0])
                        # check(model.addSpecies(final_species_hash_map[unique_species_name][0]),'adding species in combineSubsystems')
        
            check(model.getCompartment(0).setSize(total_size), 'setting compartment size in model')
        # Updating model id
        check(model.setId('combined_Subsystems_' + mod_id),'setting new model id for shared model')


  
    def connectSubsystems(self, ListOfSubsystems, connectionLogic, mode = 'volume', combineNames = False, inputSpecies = None):
        '''
        The ListOfSubsystems are combined together as in combineSubsystems 
        method (depending on combineNames). Additionally, species interaction specified 
        In the connectionLogic is modeled for the concerned Species. The inputSpecies is 
        An optional argument that may be used to specify a list of Species which are desired
        inactive in the connected Subsystem
        '''
        self.combineSubsystems(ListOfSubsystems, combineNames, mode)
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
                oldid_x = x.getId()
                oldid_y = y.getId()
                check(oldid_x,'retreiving oldid of x in connectSubsystem')
                check(oldid_y,'retreiving oldid of x in connectSubsystem')
                newid = x.getId() +'_with_' +  y.getId()
                check(newid,'retreiving newid of y in connectSubsystem')
                self.renameSId(oldid_x, newid)
                self.renameSId(oldid_y, newid)
                # Remove x from species in the model to avoid duplication
                sp_remove = model_obj.getSpeciesByName(x.getName())
                if type(sp_remove) is list:
                    print('BioSIMI-Python WARNING -- Multiple species exist in the model with the same name as given in connection logic. Ensure that connection logic deals with unique species. Simulation may lead to wrong result in this case')
                    return
                else:
                    id_to_remove = sp_remove.getId()
                    model.removeSpecies(id_to_remove)
    
    def getFastReactions(self):
        '''
        Returns the reactions in the Subsystem with the attribute fast set as True
        '''
        allReactions = self.getSubsystemDoc().getModel().getListOfReactions()
        fastReactions = []
        for reaction in allReactions:
            if reaction.isSetFast():
                if reaction.getFast() == True:
                    fastReactions.append(reaction)
        return fastReactions
    
    def setFastReactions(self, indexList):
        ''' 
        The indexList is used to set the corresponding reactions as fast
        by setting their fast attribute to True. For example, 
        indexList = [1 5], sets the 1st and 5th reaction in the Subsystem model as fast
        '''
        model = self.getSubsystemDoc().getModel()
        if type(indexList) is int:
            model.getReaction(indexList-1).setFast(True)
            return
        for index in indexList:
            model.getReaction(index-1).setFast(True)

    def getReversibleReactions(self):
        '''
        Returns the reactions in the Subsystem with the reversible attribute 
        set as True
        '''
        allReactions = self.getSubsystemDoc().getModel().getListOfReactions()
        reversibleReactions = []
        for reaction in allReactions:
            if reaction.isSetReversible():
                if reaction.getReversible():
                    reversibleReactions.append(reaction)
        return reversibleReactions

    def setReversibleReactions(self, indexList, rateFormulaList = None): 
        ''' The indexList is used to set the corresponding reactions as reversible
        by setting the reversible attribute of the reaction as True. 
        The rateFormulaList is a list of strings with math formula 
        for the new rates of the corresponding reactions that are 
        being set as reversible. Returns the new Subsystem object with changes made
        '''
        if not indexList:
            print('The list of index for reactions is empty.')
            return

        newSubsystem = self.getSystem().createNewSubsystem(3,1)
        model_orig = self.getSubsystemDoc().getModel()
        newSubsystem.getSubsystemDoc().setModel(model_orig)
        model = newSubsystem.getSubsystemDoc().getModel()
        if type(indexList) is int:
            rxn = model.getReaction(indexList-1)
            rxn.setReversible(True)
            if rateFormulaList:
                rxn.unsetKineticLaw()
                rxn_obj = NewReaction(rxn)
                formulaString = rateFormulaList
                math_ast = rxn_obj.createMath(formulaString)
                kinetic_law = rxn_obj.createRate(math_ast)
                rxn.setKineticLaw(kinetic_law)
            return newSubsystem

        for i in range(len(indexList)):
            index = indexList[i]
            rxn = model.getReaction(index-1)
            rxn.setReversible(True)
            if rateFormulaList:
                rxn.unsetKineticLaw()
                rxn_obj = NewReaction(rxn)
                formulaString = rateFormulaList[i]
                math_ast = rxn_obj.createMath(formulaString)
                kinetic_law = rxn_obj.createRate(math_ast)
                rxn.setKineticLaw(kinetic_law)
        return newSubsystem


    def unsetReversibleReactions(self, indexList, rateFormulaList = None):
        ''' The indexList is used to unset the corresponding reactions' reversible
        attribute by setting it as False. 
        The rateFormulaList is a list of strings with math formula 
        for the new rates of the corresponding reactions that are 
        being set as reversible. Returns the new Subsystem object with changes made
        '''
        if not indexList:
            print('The list of index for reactions is empty.')
            return
        newSubsystem = self.getSystem().createNewSubsystem(3,1)
        model_orig = self.getSubsystemDoc().getModel()
        newSubsystem.getSubsystemDoc().setModel(model_orig)
        model = newSubsystem.getSubsystemDoc().getModel()
        if type(indexList) is int:
            rxn = model.getReaction(indexList-1)
            rxn.setReversible(False)
            if rateFormulaList:
                rxn.unsetKineticLaw()
                rxn_obj = NewReaction(rxn)
                formulaString = rateFormulaList
                math_ast = rxn_obj.createMath(formulaString)
                kinetic_law = rxn_obj.createRate(math_ast)
                rxn.setKineticLaw(kinetic_law)
            return newSubsystem

        for i in range(len(indexList)):
            index = indexList[i]
            rxn = model.getReaction(index-1)
            rxn.setReversible(False)
            if rateFormulaList:
                rxn.unsetKineticLaw()
                rxn_obj = NewReaction(rxn)
                formulaString = rateFormulaList[i]
                math_ast = rxn_obj.createMath(formulaString)
                kinetic_law = rxn_obj.createRate(math_ast)
                rxn.setKineticLaw(kinetic_law)
        return newSubsystem


    def modelReduce(self, timepoints):
        ''' 
        Reduces the model by removing the reactions which are set as fast
        in the Subsystem model. The timepoints are used to simulate the
        fast reactions for these timepoints. The steady state values of 
        the involved species in the fast reactions are used in the
        reduced model as their initial value. 
        Returns the Subsystem object with the reduced model obtained.
        '''
        reducedSubsystem = self.getSystem().createNewSubsystem(3,1)
        model_orig = self.getSubsystemDoc().getModel()
        reducedSubsystem.getSubsystemDoc().setModel(model_orig)
        mod = reducedSubsystem.getSubsystemDoc().getModel()

        fastRxns = self.getFastReactions()
        fastSubsystem = self.getSystem().createNewSubsystem(3,1)
        fastModel = fastSubsystem.createNewModel('fastModel', mod.getTimeUnits(), mod.getExtentUnits(), mod.getSubstanceUnits() )
        # adding all global (model level) components of the model
        # to the fastModel, except reactions and species
        if mod.getNumCompartmentTypes() != 0:
            for each_compartmentType in mod.getListOfCompartmentType():
                fastModel.addCompartment(each_compartmentType)
        if mod.getNumConstraints() != 0:
            for each_constraint in mod.getListOfConstraints():
                fastModel.addConstraint(each_constraint)
        if mod.getNumInitialAssignments() != 0:
            for each_initialAssignment in mod.getListOfInitialAssignments():
                fastModel.addInitialAssignment(each_initialAssignment)
        if mod.getNumFunctionDefinitions() != 0:
            for each_functionDefinition in mod.getListOfFunctionDefinitions():
                fastModel.addFunctionDefinition(each_functionDefinition)
        if mod.getNumRules() != 0:
            for each_rule in mod.getListOfRules():
                fastModel.addRule(each_rule)
        if mod.getNumEvents() != 0:
            for each_event in mod.getListOfEvents():
                fastModel.addEvent(each_event)
        if mod.getNumCompartments() != 0:
            for each_compartment in mod.getListOfCompartments():
                fastModel.addCompartment(each_compartment)
        if mod.getNumParameters() != 0:
            for each_parameter in mod.getListOfParameters():
                fastModel.addParameter(each_parameter)
        if mod.getNumUnitDefinitions() != 0:
            for each_unit in mod.getListOfUnitDefinitions():
                fastModel.addUnitDefinition(each_unit)
        fastModel.setAreaUnits(mod.getAreaUnits())
        fastModel.setExtentUnits(mod.getExtentUnits())
        fastModel.setLengthUnits(mod.getLengthUnits())
        fastModel.setSubstanceUnits(mod.getSubstanceUnits())
        fastModel.setTimeUnits(mod.getTimeUnits())
        fastModel.setVolumeUnits(mod.getVolumeUnits())

       # adding the reactions that are fast and the species used in them to 
        # the fast model
        for rxn in fastRxns:
            fastModel.addReaction(rxn)
            mod.removeReaction(rxn.getId())
            for reactant_ref in rxn.getListOfReactants():
                fastModel.addSpecies(mod.getElementBySId(reactant_ref.getSpecies()))
            for product_ref in rxn.getListOfProducts():
                fastModel.addSpecies(mod.getElementBySId(product_ref.getSpecies()))
        
        # get equilibrium values for species in fast reactions
        # writeSBML(fastSubsystem.getSubsystemDoc(), 'models/intermediate_model.xml')
        print('###### Simulating the fast reactions in the model...All other species and parameters will be marked useless')
        time.sleep(2)
        data, m = fastSubsystem.simulateSbmlWithBioscrape(0,timepoints)
        allSpecies = fastModel.getListOfSpecies()
        for i in range(len(allSpecies)):
            species = mod.getElementBySId(allSpecies.get(i).getId())
            newAmount = data[:,m.get_species_index(species.getId())][-1]
            if newAmount > 0:
                species.setInitialAmount(newAmount)
            else:
                species.setInitialAmount(0)
        return reducedSubsystem

    def simulateSbmlWithBioscrape(self, initialTime, timepoints):
        ''' 
        To simulate SBML model without generating the plot. 
        Returns the data for all species.
        '''
        filename = 'models/temp_simulate.xml'
        writeSBML(self.getSubsystemDoc(), filename) 
        m = bioscrape.types.read_model_from_sbml(filename)
        s = bioscrape.simulator.ModelCSimInterface(m)
        s.py_prep_deterministic_simulation()
        s.py_set_initial_time(initialTime)
        sim = bioscrape.simulator.DeterministicSimulator()
        result = sim.py_simulate(s, timepoints)
        return result.py_get_result(), m

    # def simulateSbml(self, initialTime, timepoints):
    #     ''' 
    #     To simulate SBML model without generating the plot. 
    #     Returns the data for all species.
    #     '''
    #     filename = 'models/temp_simulate.xml'
    #     writeSBML(self.getSubsystemDoc(), filename) 
    #     m = bioscrape.types.read_model_from_sbml(filename)
    #     s = bioscrape.simulator.ModelCSimInterface(m)
    #     s.py_prep_deterministic_simulation()
    #     s.py_set_initial_time(initialTime)
    #     sim = bioscrape.simulator.DeterministicSimulator()
    #     result = sim.py_simulate(s, timepoints)
    #     data = result.py_get_result()
    #     return data, m
 
    def simulateVariableInputs(self, ListOfInputs, ListOfListOfAmounts, ListOfSpeciesToPlot, timepoints, mode = 'continue', xlabel = 'Time', ylabel = 'Concentration (AU)', sizeOfXLabels = 14, sizeOfYLabels = 14):
        ''''
        Simulates the Subsystem model with the input species amounts varying 
        Uses bioscrape to simulate and plots the result
        '''
        mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))
        model = self.getSubsystemDoc().getModel()
        simpleModel = SimpleModel(model)
        species_list = []
        final_result = {}
        total_time = {}
        SpeciesToPlot = ListOfSpeciesToPlot[:]
        for species_name in ListOfSpeciesToPlot:
            species = simpleModel.getSpeciesByName(species_name)
            if type(species) is list:
                print('BioSIMI-Python WARNING -- There are multiple species with the name ' + species_name + 'Suffixed species will be plotted ')
                for species_i in species:
                    species_list.append(species_i.getId())
                    final_result[species_i.getId()] = []
                    total_time[species_i.getId()] = []
                key_ind = ListOfSpeciesToPlot.index(species_name)
                insert_new = []
                for j in range(len(species)-1):
                    insert_new.append(species_name + str(j+1))
                SpeciesToPlot[key_ind+1:key_ind+1] = insert_new 
            else:
                species_list.append(species.getId())
                final_result[species.getId()] = []
                total_time[species.getId()] = []
        initialTime = timepoints[0]
        t_end = timepoints[-1]
        points = len(timepoints)
        if (len(ListOfInputs) == 1) or (type(ListOfInputs) is str):
            t = initialTime
            if type(ListOfInputs) is list:
                input = ListOfInputs[0]
            elif type(ListOfInputs) is str:
                input = ListOfInputs
            else:
                print('BioSIMI-Python ERROR -- The input species argument should either be a list or a string')
                return

            species_inp = simpleModel.getSpeciesByName(input)
            if type(species_inp) is list:
                print('BioSIMI-Python ERROR -- Multiple input species found in the model for the input name given.')
                return 
            for amount in ListOfListOfAmounts:
                if type(amount) is list:
                    print('BioSIMI-Python ERROR -- For single input, the amounts should not be a list of list type')
                    return
            for j in range(len(ListOfListOfAmounts)):
                # Start simulating and create data
                amount = ListOfListOfAmounts[j]
                check(species_inp.setInitialAmount(amount), 'setting initial amount to input species')
                time = np.linspace(t,t+t_end,points)
                data, m = self.simulateSbmlWithBioscrape(t, time)
                for species_id in species_list:
                    sp_data = data[:,m.get_species_index(species_id)]
                    t = time[-1]
                    final_result[species_id].extend(sp_data)
                    total_time[species_id].extend(time)
                if mode == 'continue':
                    for species in model.getListOfSpecies():
                        species.setInitialAmount(data[:,m.get_species_index(species.getId())][-1])




        else:
            t = initialTime
            ListOfSpecies = []
            for i in range(len(ListOfInputs)):
                input = ListOfInputs[i]
                species_inp = simpleModel.getSpeciesByName(input)
                if type(species_inp) is list:
                    print('BioSIMI-Python ERROR -- Multiple input species found in the model.')
                    return 
                ListOfSpecies.append(species_inp)
            for i in range(len(ListOfListOfAmounts)):
                if (type(ListOfListOfAmounts[i]) is not list) or (len(ListOfListOfAmounts[i]) != len(ListOfInputs)) :
                    print('BioSIMI-Python ERROR -- For multiple inputs, all items of ListOfListOfAmounts attribute should be lists of length same as the number of inputs')
                    return
            for j in range(len(ListOfListOfAmounts)):
                for amount, species in zip(ListOfListOfAmounts[j], ListOfSpecies):
                # Start simulating and create data
                    check(species.setInitialAmount(amount), 'setting initial amount to input species')
                time = np.linspace(t,t+t_end,points)
                data, m = self.simulateSbmlWithBioscrape(t, time)
                for species_id in species_list:
                    sp_data = data[:,m.get_species_index(species_id)]
                    t = time[-1]
                    final_result[species_id].extend(sp_data)
                    total_time[species_id].extend(time)

                if mode == 'continue':
                    for species in model.getListOfSpecies():
                        species.setInitialAmount(data[:,m.get_species_index(species.getId())][-1])

        for species_id in species_list:
            plt.plot(total_time[species_id], final_result[species_id])

        plt.legend(SpeciesToPlot)
        mpl.rc('xtick', labelsize= sizeOfXLabels) 
        mpl.rc('ytick', labelsize=sizeOfYLabels)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
        return final_result, total_time