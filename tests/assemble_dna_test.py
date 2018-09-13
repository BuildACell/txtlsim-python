# assemble_dna_test.py - test suite for DNA assembly
# RMM, 26 Aug 2018

import unittest
import txtl

class TestAssembleDNA(unittest.TestCase):
    
    def test_assemble_strings(self):
        mix = txtl.Mixture('testmix')
        gene = txtl.assemble_dna('ptet(50)', 'BCD2(20)', 'tetR(1200)')
        mix.write_sbml('testmix.xml')
        self.assertEqual('foo'.upper(), 'FOO')
        
        #! TODO: make sure everything was set up correctly

    def test_assemble_objects(self):
        mix = txtl.Mixture('testmix')
        
        ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True)
        bcd2 = txtl.ConstitutiveRBS('BCD2', Ribosome_Binding_F=10)
        degfp = txtl.ProteinCDS('deGFP', maturation_time=30*txtl.minutes)
        lva = txtl.DegradationTag('lva', 'clpXP')

        gene = txtl.assemble_dna(ptet, bcd2, degfp, lva)
        txtl.add_dna(mix, gene, 1, 'plasmid')
        
        #! TODO: make sure everything was set up correctly

    def test_assemble_key_value_pairs(self):
        mix = txtl.Mixture('testmix')
        gene = txtl.assemble_dna(
            prom='ptet(50)', utr5='BCD2(20)', cds='tetR(1200)')
        txtl.add_dna(mixture=mix, dna=gene, conc=1, type='plasmid')

    def test_scramble_key_value_pairs(self):  
        gene = txtl.assemble_dna(
            cds='tetR(1200)', prom='ptet(50)', utr5='BCD2(20)')
        
        #! TODO: make sure everything was set up correctly

if __name__ == '__main__':
    unittest.main()
