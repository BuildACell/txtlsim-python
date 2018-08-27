#!/usr/bin/env python
#
# parameter_test.py - test suite for setting parameters
# RMM, 26 Aug 2018

import unittest
import txtl

class TestParameters(unittest.TestCase):
    "Tests for setting txtl parameter values"

    def default_parameters(self):
        # Use default configuration information
        ptet = txtl.components.ptet

        # Create a new component with default configuration information
        ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True)

        #! TODO: make sure everything was set up correctly

    def config_file(self):
        # Overwrite system configuration file with local configuration file
        ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True,
                                      config_file='prom_ptet.csv')
        ptet = txtl.models.ptet('ptet.csv')

    def override_parameter_keyword(self):
        # Override a single parameter
        bcd2 = txtl.ConstitutiveRBS('BCD2', Ribosome_Binding_F=10)
        degfp = txtl.ProteinCDS('deGFP', maturation_time=30*txtl.minutes)

    @unittest.skip("skipping override_parameters: not yet implemented")
    def override_parameters(self):
        bcd2 = txtl.ConstitutiveRBS('BCD2',
                                    parameters = {Ribosome_Binding_F:10})

def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestParameters)

if __name__ == "__main__":
    unittest.main()
