# geneexpr.py - simple gene expression example
# Richard M. Murray, 11 Aug 2018

import txtl

# Set up the standard TXTL tubes
tube1 = txtl.extract('BL21_DE3')
tube2 = txtl.buffer('stdbuffer')

# Now set up a tube that will contain our DNA
tube3 = txtl.newtube('geneexpr')

# Define a DNA strand using strings
gene1 = txtl.assemble_dna('ptet(50)', 'BCD2(20)', 'tetR(1200)')
txtl.add_dna(tube3, gene1, 1, 'plasmid')

# Assemble a DNA strand using objects
ptet = txtl.RepressedPromoter('ptet', 'tetR')
bcd2 = txtl.ConstitutiveRBS('BCD2', Ribosome_Binding_F=10)
degfp = txtl.ProteinCDS('deGFP', maturation_time=30*txtl.minutes)
lva = txtl.DegradationTag('lva', 'clpXP')
gene2 = txtl.assemble_dna(ptet, bcd2, degfp, lva)
txtl.add_dna(tube3, gene2, 1, 'plasmid')

# Mix the contents of the individual tubes
well1 = txtl.combine_tubes([tube1, tube2, tube3])

# Run a simulation
# simData = txtl.runsim(well1, 8 * txtl.hours)

# plot the result
# txtl.plot(simData, well1)

# Create an SBML file containing the model
txtl.write_sbml(well1, 'geneexpr.sbml')
