makeSubsystem(modelSubsystemName, input, output, subsystemName)
Species:
__init__(id, name, initial_amount)


Species input_DP1 (1,'X', 2.0)
Species output_DP1 (2, 'X**', 0.0)

DP_Subsystem1 = makeSubsystem('DP', input_DP1, output_DP1, DP1)

Species input_DP2 (3, 'Y', 2.0)
Species output_DP2 (4, 'Y**', 0.0)

DP_Subsystem2 = makeSubsystem('DP', input_DP2, output_DP2, DP2)

Species input1_IFFL (5, 'pA', 2.0)
Species input2_IFFL (6, 'pB', 2.0)
Species output_IFFL (7, 'pC', 0.0)

IFFL_Subsystem = makeSubsystem('IFFL', {Species input1_IFFL, Species input2_IFFL}, output_IFFL)

Subsystem Final_Subsystem('Final_Subsystem')
connectionLogic = {}
connectionLogic[DP_Subsystem1.getOutputSpecies.getId] = IFFL_Subsystem.getInputSpecies[0].getId
connectionLogic[DP_Subsystem2.getOutputSpecies.getId] = IFFL_Subsystem.getInputSpecies[1].getId

Final_Subsystem.connect([DP_Subsystem1, DP_Subsystem2], [IFFL_Subsystem], connectionLogic)


def connect(self, [InputSubsystem], [OutputSubsystem], connectionLogic):

	final_species_hash_map = {}

	for subsystem in InputSubsystem:
		species_hash_map = {} # we dont have to bother about species in same subsystem, its amount will be correct
		for species in subsystem.getSpecies_list:
			species_hash_map[species.getId] = species

		for species_id in species_hash_map: #check if the species is present in other subsystems and store all such species
			if final_species_hash_map.get(species_id):
				final_species_hash_map[species_id].append (species_hash_map[species_id])
			else:
				final_species_hash_map[species_id] = [species_hash_map[species_id]]

	for subsystem in OutputSubsystem:
		species_hash_map = {}
		for species in subsystem.getSpecies_list:
			species_hash_map[species.getId] = species

		for species_id in species_hash_map:
			if final_species_hash_map.get(species_id):
				final_species_hash_map[species_id].append (species_hash_map[species_id])
			else:
				final_species_hash_map[species_id] = [species_hash_map[species_id]]

	for unique_species_id in final_species_hash_map: #ammend the values of same species across different subsystems
		if len(final_species_hash_map[unique_species_id]) > 1:
			Species s(unique_species_id, final_species_hash_map[unique_species_id][0], sum(final_species_hash_map[unique_species_id]))
			self.species_list.append(s)
		else:
			self.species_list.append(final_species_hash_map[unique_species_id][0])

	for species_id in connectionLogic.keys():

		 x = final_species_hash_map[species_id]
		 y = final_species_hash_map[connectionLogic[species_id]]

		 z = Species(x.getId, x.getName, sum(x.getInitial_amount, y.getInitial_amount))
		 final_species_hash_map[x.getId] = z
		 final_species_hash_map[y.getId] = z

	for subsystem in InputSubsystem:
		for reaction in subsystem.getReactions:
			for species in reaction:
				reaction.replaceSpecies(species.getSpeciesId, final_species_hash_map[species.getSpeciesId])
			Final_Subsystem.setReaction(reaction)

	for subsystem in OutputSubsystem:
		for reaction in subsystem.getReactions:
			for species in reaction:
				reaction.replaceSpecies(species.getSpeciesId, final_species_hash_map[species.getSpeciesId])
			Final_Subsystem.se
