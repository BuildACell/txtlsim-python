# extract.py - standard TX-TL extract models
# RMM, 19 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from warnings import warn

from .mixture import Mixture
from .component import Component
from .sbmlutil import add_species, add_reaction, add_parameter
from .parameter import get_parameters, eval_parameter

from .mechanisms import transcription, translation, maturation, degradation

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
    def __init__(self, name, parameters={}):
        # Save the name of the config file
        self.name = "Extract " + name
        
        # Read and store the extract parameters
        self.config_file = name.lower() + ".csv"
        self.parameters = get_parameters(self.config_file, parameters)

class StandardExtract(Extract):
    mechanisms = {
        'transcription'         : transcription.basic(),
        'translation'           : translation.basic(),
        'DNA_degradation'       : degradation.dna_basic(),
        'RNA_degradation'       : degradation.rna_basic(),
        'protein_degradation'   : degradation.protein_basic()
    }

    def update_parameters(self, mixture):
        #
        # Add in the (global) parameters that are present in the extract
        #
        # An extract should define a set of parameters that can be
        # used by all other reactions in the system.  These are added
        # at the time of species creation to insure that they are
        # available when reactions are created within components.
        #
        parameter_names = [
            # DNA degradation parameters
            'DNA_RecBCD_F', 'DNA_RecBCD_R', 'DNA_RecBCD_complex_deg',
            'GamS_RecBCD_F', 'GamS_RecBCD_R',

            # Protein degradation parameters
            'Protein_ClpXP_F', 'Protein_ClpXP_R', 'Protein_ClpXP_complex_deg',

            # RNAP binding to housekeeping promoter (if present)
            'RNAP_S70_F', 'RNAP_S70_R',

            # Translational resource utilization
            'TL_AA_F', 'TL_AA_R',
            'TL_AGTP_F', 'TL_AGTP_R',

            # Translational binding rates
            'Ribosome_Binding_F', 'Ribosome_Binding_R',

            # RNA degradation parameters
            'RNA_deg', 'RNase_F', 'RNase_R',

            # Unknown
            'NTP_F_1', 'NTP_R_1', 'NTP_F_2', 'NTP_R_2',
            'RNAPbound_termination_rate', 'Ribobound_termination_rate',

            # ATP degradation rates
            'ATP_degradation_rate', 'ATP_degradation_start_time'
        ]
        for name in parameter_names:
            # Determine the value of the parameter
            value = eval_parameter(self, name)
                
            # Create the parameter in the model
            if value != None:
                add_parameter(mixture, name, value)

    def update_species(self, mixture, conc, mechanisms={}):
        #
        # Add in the species that are present in the extract
        #
        # An extract should contain some combination of
        # transcriptional and translational machinery, although it is
        # possible to have one or none of these (eg, for a
        # transcription only system or a pure buffer with no cellular
        # machinery).
        #
        RNAP_IC = self.eval_parameter('RNAP_IC')
        if RNAP_IC != None:
            mixture.rnap = add_species(mixture, None, 'RNAP', RNAP_IC * conc)
        else:
            warn("Extract missing initial condition for species RNAP")
            mixture.rnap = add_species(mixture, None, 'RNAP', 0)
        
        Ribo_IC = self.eval_parameter('Ribo_IC')
        if Ribo_IC != None:
            mixture.ribo = add_species(mixture, None, 'Ribo', Ribo_IC * conc)
        else:
            warn("Extract missing initial condition for species Ribo")
            mixture.ribo = add_species(mixture, None, 'Ribo', 0)

        RecBCD_IC = self.eval_parameter('RecBCD_IC')
        if RecBCD_IC != None:
                 mixture.recbcd = add_species(mixture, None, 'RecBCD',
                                              RecBCD_IC * conc)

        RNase_IC = self.eval_parameter('RNase_IC')
        if RNase_IC != None:
            mixture.rnase = add_species(mixture, None, 'RNase', RNase_IC * conc)

    def update_reactions(self, mixture):
        #! TODO: add reactions that are instantiated by extract
        # mechanism['RNA_degradation'].update_reactions(mixture, mechanisms)
        None

# Create a mixture containing extract
def create_extract(name, type=StandardExtract, mechanisms={}):
    # Create a mixture to hold the extract
    mixture = Mixture(name)

    # Create the extract
    extract = type(name)

    # Add the extract as the sole contents of the tube
    mixture.components = [extract]

    #
    # Keep track of the stock concentration multiplier
    #
    # In original Noireaux paper they report concentratons in terms of
    # the total reaction volume of 10 ul, but we need to concentration
    # of the raw extract. Extract is 1/3 of the 10ul reaction volume,
    # so rescale concentration to get this to work out correctly.
    #
    #! TODO: update config files to get rid of this scaling
    #
    mixture.concentrations = [10.0/(10.0/3.0)]

    # Store default mechanisms and custom mechanisms
    mixture.default_mechanisms = extract.mechanisms
    mixture.custom_mechanisms = mechanisms

    # Store the parameters in the mixture so that components can access them
    mixture.parameters = extract.parameters

    #! TODO: read extract specific parameters
    return mixture
