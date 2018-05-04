from modules.CreateSubsystem import *
from modules.NewSubsystem import *
from modules.NewReaction import *
from modules.setIdFromNames import *

reader = SBMLReader()
check(reader,'calling sbml reader')
sbmlDoc = reader.readSBML('models/DP1_sbml.xml')
check(sbmlDoc,'reading sbml doc')
sbmlDoc1 = NewSubsystem(sbmlDoc)
sbmlDoc_new = sbmlDoc1.createNewSubsystem('new')
writeSBML(sbmlDoc_new,'DPnewtest.xml')
    # for compartments in model.getListOfCompartments():
            #     # print('i m here comp')
            #     oldid = compartments.getId()
            #     compartments.setId(oldid + NewName)
            #     oldid = compartments.getName()
            #     compartments.setName(oldid + NewName)
            #     model.addCompartment(compartments)
            # # Setting species with new names
            # for species in model.getListOfSpecies():
            #     oldid = species.getId()
            #     species.setId(oldid + NewName)
            #     oldid = species.getName()
            #     species.setName(oldid + NewName)
            #     # print('i m here species')
            #     model.addSpecies(species)
            # for reactions in model.getListOfReactions():
            #     oldid = reactions.getId()
            #     reactions.setId(oldid + NewName)
            #     oldid = reactions.getName()
            #     reactions.setName(oldid + NewName)
            #     # print('i m here rxn')
            #     model.addReaction(reactions)
            # for parameters in model.getListOfParameters():
            #     oldid = parameters.getId()
            #     parameters.setId(oldid + NewName)
            #     oldid = parameters.getName()
            #     parameters.setName(oldid + NewName)
            #     # print('i m here para')
            #     model.addParameter(parameters)
