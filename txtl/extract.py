# extract.py - standard TX-TL extract models
# RMM, 19 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .mixture import Mixture
from .component import Component
from .sbmlutil import add_species, add_reaction, add_parameter
from .parameter import load_config, eval_parameter
from .dna import dna2rna_basic  #! TODO: move mechanisms to mechanisms/
from .dna import rna2prot_basic #! TODO: move mechanisms to mechanisms/

class Extract(Component):
    """TX-TL extract component
    
    The Extract class is used to define the extract in which a set of
    TX-TL reactions are run.  The Extract class is derived from the
    Component class, but it plays a special role in that it sets the
    default mechanisms that are present in a mixture.  As such, the
    extract class should not be added to a mixture in the way of other
    components, but should instead be created using the
    `create_extract()` function (which properly initializes the
    mixture mechanisms).

    """
    def __init__(self, config_file):
        # Read the configuration parameters
        self.parameters = load_config(config_file)

        # Save the name of the config file
        self.name = "Extract " + config_file

class StandardExtract(Extract):
    def get_mechanisms(self):
        return {
            'transcription' : dna2rna_basic(),
            'translation'   : rna2prot_basic(),
        }

    def update_species(self, mixture, mechanisms={}):
        #
        # Add in the species that are present in the extract
        #
        # An extract should contain some combination of
        # transcriptional and translational machinery, although it is
        # possible to have one or none of these (eg, for a
        # transcription only system or a pure buffer with no cellular
        # machinery).
        #
        add_species(mixture, None, 'RNAP', self.parameters['RNAP_ic'].value)
        add_species(mixture, None, 'Ribo', self.parameters['Ribo_ic'].value)
        add_species(mixture, None, 'RecBCD', self.parameters['RecBCD_ic'].value)
        add_species(mixture, None, 'RNase', self.parameters['RNase_ic'].value)

        #
        # Add in the (global) parameters that are present in the extract
        #
        # An extract should define a set of parameters that can be
        # used by all other reactions in the system.  These are added
        # at the time of species creation to insure that they are
        # available when reactions are created.
        #
        parameter_names = [
            # DNA degradation parameters
            'DNA_RecBCD_Forward', 'DNA_RecBCD_Reverse', 
            'DNA_RecBCD_complex_deg',
            'GamS_RecBCD_F', 'GamS_RecBCD_R',

            # Protein degradation parameters
            'Protein_ClpXP_Forward', 'Protein_ClpXP_Reverse',
            'Protein_ClpXP_complex_deg',

            # RNAP binding to housekeeping promoter (if present)
            'RNAP_S70_F', 'RNAP_S70_R',

            # Translational resource utilization
            'TL_AA_Forward', 'TL_AA_Reverse',
            'TL_AGTP_Forward', 'TL_AGTP_Reverse',

            # Translational binding rates
            'Ribosome_Binding_F', 'Ribosome_Binding_R',

            # RNA degradation parameters
            'RNA_deg', 'RNase_F', 'RNase_R',

            # Unknown
            'NTP_Forward_1', 'NTP_Reverse_1', 'NTP_Forward_2', 'NTP_Reverse_2',
            'RNAPbound_termination_rate', 'Ribobound_termination_rate',

            # ATP degradation rates
            'ATP_degradation_rate', 'ATP_degradation_start_time'
        ]
        for name in parameter_names:
            # Make sure parameter was given in configuration file
            if self.parameters[name] != None:
                # Determine the value of the parameter
                value = eval_parameter(self.parameters[name], self.parameters)
                
                # Create the parameter in the model
                add_parameter(mixture, name, value)

    def update_reactions(self, mixture, mechanisms={}, parameters={}):
        #! TODO: add reactions that are instantiated by extract
        # mechanism['RNA_degradation'].update_reactions(mixture, mechanisms,
        #                                               parameters)
        None

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
    #! TODO: this is in the wrong place; figure out where it goes
    mixture.concentration = 10.0/(10.0/3.0)

    # Initalize the mechanisms that are represented in the extract
    mixture.mechanisms.update(extract.get_mechanisms())
    
    #! TODO: read extract specific parameters
    return mixture
