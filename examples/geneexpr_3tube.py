# geneexpr.py - simple gene expression example
# Richard M. Murray, 11 Aug 2018
#
# This example shows how to use the txtl library to create a model for
# a simple gene expression construct.  This model is constructed to
# demonstrate the ability to mimic the MATLAB TX-TL modeling toolbox
# approach as well as a few simple variants that are enabled in
# the python version.

import txtl

# Set up the standard TXTL tubes
tube1 = txtl.extract('BL21_DE3')
tube2 = txtl.buffer('stdbuffer')

# Now set up a tube that will contain our DNA
tube3 = txtl.newtube('geneexpr')

# Define a DNA strand using strings (ala MATLAB)
gene1 = txtl.assemble_dna(prom='ptet(50)', utr5='BCD2(20)', cds='tetR(1200)')
txtl.add_dna(mixture=tube3, dna=gene1, conc=1, type='plasmid')

#
# Assemble a DNA strand using objects (semi-pythonic)
#
# Note: these constructs would normally live inside of a model
# library, but this shows how to extend functionality by creating
# constructs inline.

# Create individual DNA components based on standard types
ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True)
bcd2 = txtl.ConstitutiveRBS('BCD2', Ribosome_Binding_F=10)
degfp = txtl.ProteinCDS('deGFP', maturation_time=30*txtl.minutes)
lva = txtl.DegradationTag('lva', 'clpXP')

# Assemble a gene using objects instead of strings
gene2 = txtl.assemble_dna(ptet, bcd2, degfp, lva)
txtl.add_dna(tube3, gene2, 1, 'plasmid')

# Mix the contents of the individual tubes
well1 = txtl.combine_tubes([tube1, tube2, tube3])
pass
# Run a simulation
#! TODO: implement
simdata = txtl.bioscrape.runsim(well1, 8 * txtl.hours)

# plot the result
#! TODO: implement
txtl.plot(simdata, well1, ['Protein_deGFP', 'Protein_tetR'])

# Create an SBML file containing the model
txtl.write_sbml(well1, 'geneexpr.xml')

# print out a basic report about the content of the well
well1.print_report()
