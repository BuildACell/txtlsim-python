# this function will be added in Subsystem class 
from libsbml import * 
from simpleSBMLfunctions import *
def connect(self, InputSubsystem, OutputSubsystem, connectionLogic): 
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
				#If the final hash map already has that specie name then append
				final_species_hash_map[species_name].append(species_hash_map[species_name])
			else:
				# For all the species in the dictionary not already in the final 
				# map, save them to the final map dictionary.  
				final_species_hash_map[species_name] = [species_hash_map[species_name]]
	# Same for output subsystem
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
			# If a particular species has been repeated in the above map. (That is,
			# there is/are some specie present in more than one subsystem). Then,
			# We take care of that specie(s) here by considering them all as one. 
			s_id = ""
			s_initial_amount = 0
			for i in final_species_hash_map[unique_species_name]:
				s_id += i.getId()
				s_initial_amount += i.getInitial_amount()
			# Create and add the new specie which is created to take into account
			# the multiple occurences of the common specie(s) 
			s = self.createNewSpecies(s_id, unique_species_name, sInitial = s_initial_amount)
		else:
			# If there are no species with multiple occurence in different subsystems
			# then just add the list of all species maintained in the final hash map
			# to our new subsystem's list of species.
			self.getModel().getListOfSpecies().append(final_species_hash_map[unique_species_name][0])

	# Now, we deal with second kind of interaction. That where some specie(s)
	# is activating the expression of another. This is fetch from the
	# connection logic that user gives and then the species
	# are considered bound to each other, so they maintain the same amounts
	# and go into reactions as just the one new specie 
	for species_id in connectionLogic.keys():
		# Get the ids of the concerned species from the connection logic given by the user
		 x = self.getModel().getSpecies(species_id)
		 y = self.getModel().getSpecies(connectionLogic[species_id])
		 # Create new combined specie, caused due to interaction of x and y
		 z = self.createNewSpecies(x.getId + y.getId, x.getName, sInitial = sum(x.getInitial_amount, y.getInitial_amount))
		 # Rename the new id, so that it takes effect in the species in the new model
		 self.getModel().getSpecies(species_id).renameUnitSIdRefs(species_id, z.getId) #try replacing by x and see if it works
		 self.getModel().getSpecies(connectionLogic[species_id]).renameUnitSIdRefs(connectionLogic[species_id], z.getId) # try replacing by y and see if it works