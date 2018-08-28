# geneexpr_test.py - simple gene expression unit test
# RMM, 28 Aug 2018

import unittest
import txtl

class TestGeneExpression(unittest.TestCase):

    def test_gene_expression(self):
        # Set up the standard TXTL tubes
        tube1 = txtl.extract('BL21_DE3')
        tube2 = txtl.buffer('stdbuffer')

        # Now set up a tube that will contain our DNA
        tube3 = txtl.newtube('geneexpr')

        # Define a DNA strand using strings (ala MATLAB)
        gene1 = txtl.assemble_dna('ptet(50)', 'BCD2(20)', 'tetR(1200)')
        txtl.add_dna(tube3, gene1, 1, 'plasmid')

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

        # Create an SBML file containing the model
        txtl.write_sbml(well1, 'geneexpr.xml')

        #! TODO: test to make sure the model is valid

if __name__ == '__main__':
    unittest.main()
