from libsbml import *
import libsbml
import bioscrape
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from modules.SimpleModel import *

def getFromXML(filename):
    """ Returns the SBMLDocument object from XML file given """
    reader = SBMLReader()
    doc = reader.readSBML(filename)
    check(doc, "reading from SBML file")
    return doc

def createSubsystemDoc(newLevel, newVersion):
    try:
        sbmlDoc = SBMLDocument(newLevel, newVersion)
    except ValueError:
        print('Could not create SBMLDocument object')
        sys.exit(1)
    return sbmlDoc


def plotSbmlWithBioscrape(filename, initialTime, timepoints, ListOfSpeciesToPlot, xlabel, ylabel, sizeOfXLabels, sizeOfYLabels):
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
    # print(ListOfSpeciesToPlot[1])
    for i in range(len(ListOfSpeciesToPlot)):
        species_name = ListOfSpeciesToPlot[i]
        species_id = mod_obj.getSpeciesByName(species_name).getId()
        species_ind.append(m.get_species_index(species_id))
    sim = bioscrape.simulator.DeterministicSimulator()
    result = sim.py_simulate(s, timepoints)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(len(species_ind)):
        plt.plot(timepoints, result.py_get_result()[:, species_ind[i]])
        # plt.legend(m.get_species_list()[species_ind[i]])
        plt.legend(ListOfSpeciesToPlot)
    plt.show()

class Subsystem(object):

    def __init__(self, SubsystemDoc):
        self.SubsystemDoc = SubsystemDoc
        
    def getSubsystemDoc(self):
        return self.SubsystemDoc

    # def renameSId (document, oldSId, newSId): 
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
        document = self.getSubsystemDoc()
        allElements = document.getListOfAllElements()
        result = []
        if (allElements == None or allElements.getSize() == 0):
            return result 

        for i in range (0, allElements.getSize()):
            current = allElements.get(i) 
            if (current.isSetId() and current.getTypeCode() != libsbml.SBML_LOCAL_PARAMETER):
                result.append(current.getId()) 
        return result     
 
    def suffixAllElementIds(self, name):
        """ Takes the subsystem name (SubName) given and returns a copy of the subsystem
            given in the SBMLDocument object in the SubsystemDoc attribute
        """
        document = self.getSubsystemDoc()
        allids = self.getAllIds()
        for oldid in allids:
            self.renameSId(oldid, oldid + '_' + name)

        # Use if want to rename all names too
        # elements = document.getListOfAllElements()
        # for element in elements:
        #     if element.isSetName():
        #         oldname = element.getName()
        #         newname = oldname + '_' + name
        #         element.setName(newname)

        return document

    def setSubsystemCompartments(self, newCompartments):
        document = self.getSubsystemDoc()
        compartments = document.getModel().getListOfCompartments()
        if len(compartments) != len(newCompartments):
            print('Warning : - The number of compartments given is not the same as the number of compartments in the model.') 
            for i in range(len(newCompartments)):
                # rename compartment name and id
                if compartments.get(i).isSetName():
                    compartments.get(i).setName(newCompartments[i])
                oldid = compartments.get(i).getId()
                self.renameSId(oldid,newCompartments[i])   
   
        else:
            for i in range(len(compartments)):
                # rename compartment name and id
                if compartments.get(i).isSetName():
                    compartments.get(i).setName(newCompartments[i])
                oldid = compartments.get(i).getId()
                self.renameSId(oldid,newCompartments[i])   
   
    def createNewModel(self, modelId, timeUnits, extentUnits, substanceUnits):
        model = self.getSubsystemDoc().createModel()
        if model == None:
            # Do something to handle the error here.
            print('Unable to create Model object.')
            sys.exit(1)
        status = model.setId(modelId)
        if status != LIBSBML_OPERATION_SUCCESS:
            # Do something to handle the error here.
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
        model_base = ListOfSubsystems[0].getSubsystemDoc().getModel()
        model = self.createNewModel('connected_model',model_base.getTimeUnits(), model_base.getExtentUnits(), model_base.getSubstanceUnits())
        document.setModel(model)

        # Adding parameters, unit definitions, reactions
        for subsystem in ListOfSubsystems:
            mod = subsystem.getSubsystemDoc().getModel()
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

    def combineSubsystems(self, ListOfSubsystems, combineNames):
        self.mergeSubsystemModels(ListOfSubsystems)
        model = self.getSubsystemDoc().getModel()
        for subsystem in ListOfSubsystems:
            mod = subsystem.getSubsystemDoc().getModel()
            if combineNames == False:
                if mod.getNumSpecies() != 0:
                  for each_species in mod.getListOfSpecies():
                      model.addSpecies(each_species)

        # The final species hash map is a dictionary for all the species that will be
        # in the final subsystem.
        if combineNames == True:
            final_species_hash_map = {}
            for subsystem in ListOfSubsystems:
                # Set the list of reactions in the final subsystem. Get the list of
                # reactions in the input subsystem and set it to final subsystem
                species_hash_map = {}
                for species in subsystem.getSubsystemDoc().getModel().getListOfSpecies():
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
                if len(final_species_hash_map[unique_species_name]) > 1:
                    # For any species with same name 
                    # which were present in more than one subsystem
                    cumulative_amount = 0
                    count = 0
                    for i in final_species_hash_map[unique_species_name]:
                        cumulative_amount += i.getInitialAmount()
                        if count >= 1:
                            uni_sp = final_species_hash_map[unique_species_name][count]
                            oldid = uni_sp.getId()
                            model.getListOfSpecies().remove(uni_sp.getId())
                        else:
                            uni_sp = final_species_hash_map[unique_species_name][count]
                            model.getListOfSpecies().append(uni_sp)
                            oldid_keep = uni_sp.getId()
                            oldid = uni_sp.getId()
                        newid = oldid_keep + 'multiple'
                        self.renameSId(oldid, newid )
                        count += 1
                    model.getSpecies(newid).setInitialAmount(cumulative_amount)
                else:
                    # If there are no species with multiple occurence in different subsystems
                    # then just add the list of all species maintained in the final hash map
                    # to our new subsystem's list of species.
                    model.getListOfSpecies().append(final_species_hash_map[unique_species_name][0])


    def shareSubsystems(self, ListOfSubsystems, ListOfSharedResources):
        self.mergeSubsystemModels(ListOfSubsystems)
        model = self.getSubsystemDoc().getModel()
        mod_obj = SimpleModel(model)
       # subsystem and set it to final subsystem
        final_species_hash_map = {}
        for subsystem in ListOfSubsystems:
            # Set the list of reactions in the final subsystem. Get the list of
            # reactions in the input subsystem and set it to final subsystem
            species_hash_map = {}
            for species in subsystem.getSubsystemDoc().getModel().getListOfSpecies():
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
            count = 0
            uni_sp = final_species_hash_map[unique_species_name][count]
            if len(final_species_hash_map[unique_species_name]) > 1:
                # For any species with same name 
                # which were present in more than one subsystem
                for i in final_species_hash_map[unique_species_name]:
                    if count >= 1 and uni_sp.getName() in ListOfSharedResources:
                        cumulative_amount += i.getInitialAmount()
                        oldid = uni_sp.getId()
                        model.getListOfSpecies().remove(uni_sp.getId())
                        newid = oldid
                    else:
                        cumulative_amount = i.getInitialAmount()
                        # uni_sp = final_species_hash_map[unique_species_name][count]
                        model.getListOfSpecies().append(uni_sp)
                        oldid_keep = uni_sp.getId()
                        oldid = uni_sp.getId()
                        newid = oldid
                    if uni_sp.getName() in ListOfSharedResources:
                        newid = oldid_keep + 'multiple'
                        self.renameSId(oldid, newid )
                    count += 1
                model.getSpecies(newid).setInitialAmount(cumulative_amount)
            else:
                # If there are no species with multiple occurence in different subsystems
                # then just add the list of all species maintained in the final hash map
                # to our new subsystem's list of species.
                model.getListOfSpecies().append(final_species_hash_map[unique_species_name][0])

   
        writeSBML(self.getSubsystemDoc(),'models/DP_IFFL_connected.xml')


  
    def connectSubsystems(self, ListOfSubsystems, combineNames, connectionLogic, inputSpecies):

        self.combineSubsystems(ListOfSubsystems, combineNames)
        model = self.getSubsystemDoc().getModel()
    # The connection logic given by user species two or more different species
    # but that are bound to each other.
        # Set the initial amount of the input in the output subsystem to zero since it's not
        # isolated anymore.
        model_obj = SimpleModel(model)
        model_obj.getSpeciesByName(inputSpecies).setInitialAmount(0.0)
        for species_name in connectionLogic.keys():
            # Get the ids of the concerned species from the
            # connection logic given by the user
            x = model_obj.getSpeciesByName(species_name)
            y = model_obj.getSpeciesByName(connectionLogic[species_name])
            if x.getCompartment() == y.getCompartment():
                s = sum([x.getInitialAmount(), y.getInitialAmount()])
                # x and y should also have the same id so that they go into reactions as one.
                # Also, set the initial amount of the species to be equal to the
                # sum of their individual amounts
                x.setName(y.getName())
                x.setInitialAmount(s)
                y.setInitialAmount(s)
                # Rename ID of x by that of y
                oldid = x.getId()
                newid = y.getId()
                self.renameSId(oldid, newid)