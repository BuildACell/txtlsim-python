from libsbml import * 
import libsbml

class Subsystem(object):
    """
        Attributes:
            model: A subsystem model object   
    """

    def __init__(self, model):
        """Return a Subsystem object whose model is "model".""" 
        self.model = model

    def getModel():
        """Return the model of the subsystem"""
        return self.model

    def setModel(self, model):
        """Set the subsystem's model"""
        self.model = model

    def check(value, message):
        """If 'value' is None, prints an error message constructed using
        'message' and then exits with status code 1.  If 'value' is an integer,
        it assumes it is a libSBML return status code.  If the code value is
        LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
        prints an error message constructed using 'message' along with text from
        libSBML explaining the meaning of the code, and exits with status code 1.
        """
        if value == None:
             raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
        elif type(value) is int:
            if value == LIBSBML_OPERATION_SUCCESS:
               return
            else:
               err_msg = 'Error encountered trying to ' + message + '.' \
                         + 'LibSBML returned error code ' + str(value) + ': "' \
                         + OperationReturnValue_toString(value).strip() + '"'
               raise SystemExit(err_msg)
        else:
            return

    def createNewCompartment(self, cId, cName, cSize, cUnits, cConstant ):
        """"Return the new compartment of the model"""
        model = self.getModel()
        comp_obj = model.createCompartment()
        check(comp_obj,'Create comp_obj compartment')
        check(comp_obj.setId(cId), 'Set comp_obj id')
        check(comp_obj.setName(cName),'Set comp_obj name')
        check(comp_obj.setSize(cSize),'set comp_obj size')
        check(comp_obj.setUnits(cUnits),'set comp_obj units')
        check(comp_obj.setConstant(cConstant),'set comp_obj constant')
        return comp_obj

    def createNewSpecies(self,sId,sName,sComp,sInitial,sConstant,sBoundary,sSubstance,sHasOnlySubstance):
        """Return the new species of the model"""
        model = self.getModel()
        s_obj = model.createSpecies()
        check(s_obj,'created s_obj species')
        check(s_obj.setId(sId),'set s_obj ID')
        check(s_obj.setName(sName),'set s_obj name')
        check(s_obj.setCompartment(sComp),'set s_obj compartment')
        check(s_obj.setInitialAmount(sInitial),'set s_obj initial amount')
        check(s_obj.setConstant(sConstant),'set s_obj constant')
        check(s_obj.setBoundaryCondition(sBoundary),'set boundary s_obj condition false')
        check(s_obj.setSubstanceUnits(sSubstance),'set substance units s_obj')
        check(s_obj.setHasOnlySubstanceUnits(sHasOnlySubstance),'set has only substance units s_obj')
        return s_obj

    def createNewReaction(self,rId,rReversible,rFast):
        """Return new reaction object"""
        model = self.getModel()
        r_obj = model.createReaction()
        check(r_obj,'created r_obj reaction')
        check(r_obj.setId(rId),'set r_obj ID')
        check(r_obj.setReversible(rReversible),'set r_obj reversible')
        check(r_obj.setFast(rFast),'set r_obj Fast')
        return r_obj

    def connect(self, InputSubsystem, OutputSubsystem, connectionLogic): 
        # The final species hash map is a dictionary for all the species that will be 
        # in the final subsystem.
        final_species_hash_map = {}
        for subsystem in InputSubsystem:
            # Set the list of reactions in the final subsystem. Get the list of
            # reactions in the input subsystem and set it to final subsystem
            self.getModel().setListOfReaction(subsystem.getModel().getListOfReaction())
            species_hash_map = {} 
            for species in subsystem.getModel().getListOfSpecies():
                # Maintain the dictionary for all species in the input subsystems by their name
                species_hash_map[species.getName()] = species
            for species_name in species_hash_map: 
                if final_species_hash_map.get(species_name):
                    #If the final hash map already has that species then append to 
                    # the same instead of duplicating
                    final_species_hash_map[species_name].append(species_hash_map[species_name])
                else:
                    # For all the species in the dictionary not already in the final 
                    # hash map, save them to the final hash map dictionary.  
                    final_species_hash_map[species_name] = [species_hash_map[species_name]]
        # Do the same for output subsystem
        for subsystem in OutputSubsystem:
            self.getModel().setListOfReaction(subsystem.getModel().getListOfReaction())
            species_hash_map = {}
            for species in subsystem.getModel().getListOfSpecies():
                species_hash_map[species.getName] = species
            for species_name in species_hash_map:
                if final_species_hash_map.get(species_name):
                    final_species_hash_map[species_name].append(species_hash_map[species_name])
                else:
                    final_species_hash_map[species_name] = [species_hash_map[species_name]]
        for unique_species_name in final_species_hash_map: 
            if len(final_species_hash_map[unique_species_name]) > 1:
                # For any species which were present in more than one subsystem
                # A new species s is created with new id and cumulative amount in the 
                # final subsystem.
                s_id = ""
                s_initial_amount = 0
                for i in final_species_hash_map[unique_species_name]:
                    s_id += i.getId()
                    s_initial_amount += i.getInitial_amount()
                    uni_sp = final_species_hash_map[unique_species_name][0]
                # Create and add the new species which is created to take into account
                # the multiple occurences of the common species(s) 
                s = self.createNewSpecies(s_id, unique_species_name, uni_sp.getCompartment(), s_initial_amount, uni_sp.getConstant(), uni_sp.getBoundaryCondition(), uni_sp.getSubstanceUnits(), uni_sp.getHasOnlySubstanceUnits())
            else:
                # If there are no species with multiple occurence in different subsystems
                # then just add the list of all species maintained in the final hash map
                # to our new subsystem's list of species.
                self.getModel().getListOfSpecies().append(final_species_hash_map[unique_species_name][0])

    # The connection logic given by user species two or more different species
    # but that are bound to each other.
    #  A new species z is created to account for this species interaction.
        for species_id in connectionLogic.keys():
            # Get the ids of the concerned species from the connection logic given by the user
            x = self.getModel().getSpecies(species_id)
            y = self.getModel().getSpecies(connectionLogic[species_id])
            # Create new combined species, caused due to interaction of x and y
            z = self.createNewSpecies(x.getId + y.getId, x.getName, x.getCompartment(), sum(x.getInitial_amount, y.getInitial_amount), x.getConstant(), x.getBoundaryCondition(), x.getSubstanceUnits(), x.getHasOnlySubstanceUnits())
            # Rename the new id, so that it takes effect in the species in the new model
            self.getModel().getSpecies(species_id).renameUnitSIdRefs(species_id, z.getId) #try replacing by x and see if it works
            self.getModel().getSpecies(connectionLogic[species_id]).renameUnitSIdRefs(connectionLogic[species_id], z.getId) # try replacing by y and see if it works       #copy the code here





