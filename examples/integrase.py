# integrase.py - integrase example
# RMM, 20 Aug 2018 (based on psuedo-code from W. Poole)
#
# This example shows how to use the txtl library to create a model for
# an integrase that flips a promoter between two different
# orientations, one of which expresses GFP and the other that
# expresses RFP.

import txtl

# Import mechanism libraries
import txtl.mechanisms as ML1
import examples.mechanisms as ML2

# Extract and Energy Parameters are stored in a user curated CSV
#! TODO: mixture + mixture -> mixture
myRXN = txtl.extract('BL21_DE3') + txtl.buffer('stdbuffer')

# Define the DNA assembly that the integrase acts on
flip_gene = txtl.FlippableAssembly(promoter='ptet', utr5=['BCD2', 'BCD2'],
                                   cds=['GFP', 'RFP'], integrase="Bxb1",
                                   translation=ML2.translation)

integrase_gene = txtl.DNAassembly(promoter='pMedium', utr5='bcd8', cds='Bxb1',
                                  translation=ML2.translation)

# Put in 10 nM of the flippable construct, 2 nM of the integrase DNA
#! TODO: scalar * construct -> mixture
myRXN += 10*flip_gene + 2*integrase_gene

# Define the mechanisms/variants to be used in instantiating the model
#! TODO: not sure if this can/should be implemented in this way.
#! Might need to use a dictionary instead?
myRXN.mechanisms += = [ML.integrases, ML.sigma70_transcription,
                       ML2.translation, ML.first_order_mRNA_degredation,
                       ML.enzymatic_energy_consumption] 

# Should return some kind of easily readable/analyzable data structure
# CRN = myRXN.compile_crn() 

# Returns SBML text and possibly also saves an SBML file
SBML = myRXN.write_sbml(myRXN, 'integrase.sbml')

# Not necessary, but might be nice to have automatic integration with BioSCRAPE
# ResultsODE = myRXN.simulate_with_bioscrape_ode(time = 10) 
# ResultsSSA = myRXN.simulate_with_bioscrape_SSA(volume = 5, time = 10)
