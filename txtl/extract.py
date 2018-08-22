# extract.py - standard TX-TL extract models
# RMM, 19 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .mixture import Mixture
from .sbmlutil import add_species, add_reaction, add_parameter
from .config import load_config

class Extract:
    def __init__(self, config_file):
        # Read the configuration parameters
        self.params = load_config(config_file)

        # Save the name of the config file
        self.name = "Extract " + config_file

class StandardExtract(Extract):
    def update_species(self, model):
        # Add in the species that are present in the extract
        add_species(model, None, 'RNAP', self.params['RNAP_ic'].value)
        add_species(model, None, 'Ribo', self.params['Ribo_ic'].value)
        add_species(model, None, 'RecBCD', self.params['RecBCD_ic'].value)
        add_species(model, None, 'RNase', self.params['RNase_ic'].value)

        # Add in the (global) parameters that are present in the extract
        parameter_names = [
            'DNA_RecBCD_Forward', 'DNA_RecBCD_Reverse',
            'DNA_RecBCD_complex_deg',
            'Protein_ClpXP_Forward', 'Protein_ClpXP_Reverse',
            'Protein_ClpXP_complex_deg',
            'RNAP_S70_F', 'RNAP_S70_R',
            'GamS_RecBCD_F', 'GamS_RecBCD_R',
            'TL_AA_Forward', 'TL_AA_Reverse',
            'TL_AGTP_Forward', 'TL_AGTP_Reverse',
            'Ribosome_Binding_F', 'Ribosome_Binding_R',
            'RNA_deg', 'RNase_F', 'RNase_R',
            'NTP_Forward_1', 'NTP_Reverse_1', 'NTP_Forward_2', 'NTP_Reverse_2',
            'RNAPbound_termination_rate', 'Ribobound_termination_rate',
            'ATP_degradation_rate', 'ATP_degradation_start_time'
        ]
        for name in parameter_names:
            # Make sure parameter was given in configuration file
            if self.params[name] != None:
                # Create the parameter
                add_parameter(model, name, self.params[name].value)

    def update_reactions(self, model, mechanisms={}):
        #! TODO: add reactions that are instantiated by extract
        return None

# Create a mixture containing extract
def create_extract(name, type=StandardExtract):
    # Create a mixture to hold the extract
    mixture = Mixture(name)

    # Create the extract
    extract = type(name)

    # Add the extract as the sole contents of the tube
    mixture.components = [extract]

    # Keep track of the stock concentration multiplier
    # Extract is 1/3 of the 10ul reaction volume
    mixture.concentration = 10.0/(10.0/3.0)
    
    #! TODO: read extract specific parameters
    return mixture
