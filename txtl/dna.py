# dna.py - DNA class and related functions
# RMM, 11 Aug 2018
#
# This file contains the implementation of DNA in the txtlsim toolbox.
# This includes objects that represent the individual elements of a
# DNA assembly as well as the functions required to create the models
# associated with gene expression.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import re                      # use Python's regular expression library
from math import log
from .component import Component
from .sbmlutil import add_species, add_reaction, find_species
from .mechanism import Mechanism, get_mechanisms
from .pathutil import load_model
from .parameter import get_parameters, update_existing, update_missing
from .mechanisms import maturation

#
# DNA assembly
#
# The DNAassembly class is a non-standard component that consists of a
# collection of DNA subcomponents.  A mechanism dictionary is
# maintained at the assembly level, but can be overriden at the
# component level.  Parameter dictionaries for DNA assembly are stored
# in the individual elements and not at the assembly level, but the
# `assemble_dna()` function can process assembly wide parameters.
#
# DNA elements that are part of an assembly have a data attribute
# `assy` that points back to the assembly that the element is part of.
# This attribute is initialized by the `DNAassembly.update_species()`
# function (before calling the individual update functions for the DNA
# elements).  Note that this means that the `assy` attribute is not
# available in the element initializer (since we don't yet know what
# assembly we will be part of).
#

class DNAassembly(Component):
    """DNA assembly class

    The DNA assembly class is used to represent a collection of DNA
    subcomponents, typically consisting of a promoter, a ribosome
    binding site (5' UTR), a protein coding sequence (CDS), an
    optional C-terminus tag (for protein degradation), and a
    terminator (3' UTR).  Subclasses can be used to create specialized
    types of DNA and predefined subclasses are available for
    promoters, RBSs, etc.

    The DNA assembly follows the rules of a Component but it is more
    complex because each of the elements of the assembly
    (subcomponents) have their own functions.  As a consequence, most
    of what the assembly construct does is to keep track of the
    individual subcomponents and calls on those subcomponent to
    generate species and reactions.

    Data attributes
    ---------------
    name        Name of the sequence (str)
    promoter    Promoter sequence (DNA)
    utr5        5' UTR (DNA)
    cds         Coding sequence (DNA) 
    ctag        C-terminus tag (DNA)
    utr3        3' UTR (DNA)

    dnalength   Length of the entire sequence (int)
    rnalength   Length of the transcribed components (int)
    peplength   Lenth of the translated components (int)

    rnaname     Name of the RNA species (str) [not implemented]
    rnap        RNAP species (SMBLspecies) [not implemented]
    riboname    Name of the ribosome species (str) [not implemented]
    ribo        Ribosome species [not implemented]

    default_mechanisms  default mechanisms for generating models
    custom_mechanisms   customized mechanisms for generating models

    parameters  Parameter values for the assembly (overrides elements)

    Methods
    -------
    update_species()    create/update species associated with construct
    update_reactions()  create/update reactions associated with construct

    """
    def __init__(
        self, name,
        promoter=None, utr5=None, cds=None, ctag=None, utr3=None,
        mechanisms={},                     # custom mechanisms
        config_file=None, parameters={},   # parameter configuration
        **keywords                         # parameter keywords
    ):
        self.name = name
        self.promoter = promoter
        self.utr5 = utr5
        self.cds = cds
        self.ctag = ctag
        self.utr3 = utr3

        # Keep track of the length of DNA, RNA, and protein (peptide)
        self.dnalength = 0
        self.rnalength = 0
        self.peplength = 0

        # Set up the default mechanisms for a DNA assembly
        # Note: transcription, translation, degradation are given by extract
        self.default_mechanisms = {
            'maturation' : maturation.protein_basic()
        }
        self.custom_mechanisms = mechanisms

        # Create the config_file name (optional)
        if config_file == None and isinstance(name, str):
            config_file = self.name.lower() + ".csv"
        self.config_file = config_file
        
        # Set the assembly parameter values (processed by assemble_dna())
        self.parameters = get_parameters(
            config_file, parameters, None, **keywords)

    # Create/update all of the species associated with this DNA assembly
    def update_species(self, mixture, conc, debug=False):
        # Create the DNA species
        self.dna = add_species(mixture, "DNA", self.name, conc)

        # Let the individual DNA elements create the additional species
        for dna in [self.promoter, self.utr5, self.cds, self.ctag, self.utr3]:
            if dna != None:
                # Store the DNA assembly that generated this component
                dna.assy = self

                # Update the species required for this component
                if debug: print("DNAassembly species update:", dna.name)
                dna.update_species(mixture, conc)

    # Create/update all of the relevant reactions for this DNA assembly
    def update_reactions(self, mixture, debug=False):
        # Go through each subcomponent and update reactions
        for dna in [self.promoter, self.utr5, self.cds, self.ctag, self.utr3]:
            if dna != None:
                dna.update_reactions(mixture)
            
#
# DNA component
#
# DNA elements will generally using the `DNA.__init__()` function to
# initialize the object.  To accommodate default parameter
# dictionaries for tthe subclasses, an additional argument
# (`default_parameters`) is available.
#

class DNA(Component):
    """DNA class

    The DNA class is used to represent a DNA sequence that has a given
    length.  Its main purpose is as the parent object for DNA
    fragments and DNA assemblies.

    Note: for initialization of members of this class, the arguments
    should be as follows:

      DNA(name, length, [mechanisms], [config_file], [prefix])

        DNAtype(name, required_arguments, [length], [mechanisms], 
                [config_file], [prefix], [optional_arguments])

          DNAelement(name, required_arguments, [length], [mechanisms], 
                     [config_file], [optional_arguments])

      DNAtypes - DNAelements:
        Promoter - ConstitutePromoter, RepressedPromoter
        UTR5     - ConstituteRBS
        CDS      - ProteinCDS
        Ctag     - DegrationTAg
        UTR3     - Terminator

    Data attributes
    ---------------
    name        Name of the sequence (str)
    length      Length of the sequence (int)
    assy        DNA assembly that we are part of
    mechanisms  Local mechanisms for this component (overrides defaults)
    parameters  Parameter dictionary for the DNA element

    """
    def __init__(
        self, name, length=0,             # positional arguments
        mechanisms={},                    # custom mechanisms
        config_file=None, parameters={},  # customized parameters
        default_parameters = {},          # element parameters
        prefix="dna_", **keywords
    ):
        self.name = name
        self.length = length
        self.mechanisms = mechanisms
        self.prefix = prefix

        # Create the config_file name (optional)
        if config_file == None and isinstance(name, str):
            config_file = prefix + self.name.lower() + ".csv"
        self.config_file = config_file
        
        # Load and store the parameters for this component
        self.parameters = get_parameters(
            config_file, parameters, default_parameters, **keywords)

    # Set up default update functions to do nothing
    def update_species(self, mixture, conc):
        return None
    
    def update_reactions(self, mixture):
        return None

#
# Promoter subclasses
#
# The promoter subclasses are used to create standard promoters
# (constitutive, repressed, activated).  When creating an instance of
# one of these subclasses, the name of the transcriptional regulator
# (if any) is passed as an argument and the appropriate reactions are
# instantiated.
#

# Promoter sequence
class Promoter(DNA):
    "Promoter class - define a promoter sequence"

    # Default parameters used to describe a promoter
    default_parameters = {
        'RNAPbound_F' : 20,       # Default for ptet
        'RNAPbound_R' : 400       # Default for ptet
    }
    
    def __init__(
        self, name, length=50,
        mechanisms={}, config_file=None, parameters={},
        default_parameters = default_parameters,
        rnapname="RNAP", prefix="prom_", **keywords
    ):
        # Promoter initialization (including mechanisms and parameters)
        DNA.__init__(
            self, name, length=length, mechanisms=mechanisms,
            config_file=config_file, parameters=parameters,
            default_parameters = default_parameters,
            prefix=prefix, **keywords)

        # Set (or reset) values based on function arguments
        self.rnapname = rnapname

        # Fill in any missing parameter values with defaults
        update_missing(self.parameters, Promoter.default_parameters)

    def update_species(self, mixture, conc, parameters={}):
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the mRNA species
        assy.rnaname = assy.utr5.name + "--" + assy.cds.name
        if (assy.ctag != None): assy.rnaname += "--" + assy.ctag.name
        assy.rna = add_species(mixture, "RNA", assy.rnaname, 0)

        # Create RNA polymerase bound to DNA
        assy.rnap_bound = add_species(mixture, "Complex",
                                      self.rnapname + ":" + assy.name, 0)

        # Create any other species needed by the transcriptional machinery
        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['transcription'].update_species(mixture, assy, conc)
        
    # Default action of a promoter is to implement transcription
    def update_reactions(self, mixture, debug=False):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the reactions required for transcription
        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['transcription'].update_reactions(mixture, assy)

# Constitute promoter
class ConstitutivePromoter(Promoter):
    "ConstitutivePromoter - define a constitutive promoter"

# Repressed promoter
class RepressedPromoter(Promoter):
    #! TODO: add docstring
    
    # Default parameters used to describe a repressed promoter
    default_parameters = {
        'RNAPbound_F'        : 20,      # Default for ptet
        'RNAPbound_R'        : 400,     # Default for ptet
        'DNAsequestration_F' : 2.5e-1,  # Default for ptet
        'DNAsequestration_R' : 1.11e-4, # Default for ptet
    }
    
    def __init__(
        self, name, repressor, length=50,
        mechanisms={}, config_file=None, parameters={},
        rnapname="RNAP", dimer=False, **keywords
    ):
        # Promoter initialization (including mechanisms and parameters)
        Promoter.__init__(
            self, name, length=length, mechanisms=mechanisms,
            config_file=config_file, parameters=parameters,
            default_parameters = RepressedPromoter.default_parameters,
            rnapname=rnapname, **keywords)

        # Store additional information related to repression
        self.tfname = "Protein " + repressor
        if dimer: self.tfname += " dimer" 
        self.dimer = dimer

    def update_species(self, mixture, conc):
        assy = self.assy        # Get the DNA assembly we are part of

        # Create species for unrepressed promoter
        Promoter.update_species(self, mixture, conc)

        # Create repressor bound to DNA
        self.tf_bound = add_species(mixture, "Complex",
                                    self.tfname + ":" + assy.name, 0)

        # mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        # mechanisms['process'].update_species(mixture, assy, conc)

    def update_reactions(self, mixture, debug=False):
        model = mixture.model     # Get the model where we will store results
        assy = self.assy          # Get the DNA assembly we are part of
        params = self.parameters  # Get the parameter dictionary

        # Create the reactions for the unbound promoter
        Promoter.update_reactions(self, mixture)

        # Create the reaction for the transcription factor binding to DNA
        tf_species = find_species(mixture, self.tfname)
        if tf_species == None:
            raise NameError("RepressedPromoter: %s not found" % self.tfname)
        add_reaction(mixture, [tf_species, assy.dna], [self.tf_bound],
                     kf = params['DNAsequestration_F'],
                     kr = params['DNAsequestration_R'])

        # mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        # mechanisms['process'].update_reactions(mixture, assy)

#
# UTR5 subclasses
#
# The UTR5 subclasses are used to create ribosome binding sites (RBSs).

class UTR5(DNA):
    "UTR5 class - define 5' untranslated region sequence"

    # Default parameters used to describe a UTR5 (empty)
    default_parameters = {}
    
    def __init__(
        self, name, length=20,
        mechanisms={}, config_file=None, parameters={},
        default_parameters = default_parameters,
        prefix="utr5_", **keywords
    ):
        DNA.__init__(
            self, name, length, mechanisms=mechanisms,
            config_file=config_file, parameters=parameters,
            default_parameters = default_parameters,
            prefix=prefix, **keywords)        

# Constitutive RBS
class ConstitutiveRBS(UTR5):
    #! TODO: add docstring
    
    # Default parameters used to describe a constitutive RBS (TODO)
    default_parameters = {
        'Ribosome_Binding_F' : 0.1,     # TODO: add source information
        'Ribosome_Binding_R' : 4,       # TODO: add source information
    }
    
    def __init__(
        self, name, length=20,
            mechanisms={}, config_file=None, parameters={},
            riboname = 'Ribo',          # Ribosome species name
            **keywords                  # Additional keywords
    ):
        UTR5.__init__(
            self, name, length=length, mechanisms=mechanisms,
            config_file=config_file, parameters=parameters,
            default_parameters = ConstitutiveRBS.default_parameters,
             **keywords)
        self.riboname = riboname

    def update_species(self, mixture, conc, parameters={}):
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the protein
        assy.protname = assy.cds.name
        if (assy.ctag != None): assy.protname += "--" + assy.ctag.name
        assy.protein = add_species(mixture, "Protein", assy.protname, 0)

        # Create Ribosome bound to RNA
        assy.ribo_bound = add_species(mixture, "Complex",
                                      self.riboname + ":" + assy.rnaname, 0)
        
        # Create any other species needed by the transcriptional machinery
        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['translation'].update_species(mixture, assy, conc)

    # Default action of a promoter is to implement transcription
    def update_reactions(self, mixture, debug=False):
        assy = self.assy        # Get the DNA assembly we are part of
        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['translation'].update_reactions(mixture, assy)
        
#
# CDS subclasses
#
# The CDS subclasses are used to create proteins and peptides
#
#! Sort out whether we need anything more than CDS

class CDS(DNA):
    "CDS class - define protein coding sequence"
    
    # Default parameters used to describe a repressed promoter
    default_parameter_values = {
        'Dimerization_F' : 1,                   # Default for TetR
        'Dimerization_R' : 1,                   # Default for ptet
        'Protein_Maturation' : log(2)/(5*60)    # 5 minutes (GFP)
    }
    
    def __init__(
        self, name, length=1000,
        mechanisms={}, config_file=None, parameters={},
        dimerize = False, maturation_time=None,
        **keywords
    ):
        # DNA initialization
        DNA.__init__(
            self, name, length=length,mechanisms=mechanisms,
            config_file=config_file, parameters=parameters,
            default_parameters = CDS.default_parameter_values,
            prefix="cds_", **keywords)
        self.dimerize = dimerize
        self.maturation_time = maturation_time
        
    def update_species(self, mixture, conc, parameters={}):
        assy = self.assy        # Get the DNA assembly we are part of

        # Create species for the protein
        self.protein = add_species(mixture, "Protein", self.name, 0)
        if self.dimerize:
            #! Move to mechanism function?
            self.dimer = add_species(mixture, "Protein",
                                     self.name + " dimer", 0)

        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['maturation'].update_species(mixture, assy, conc)

    # Default action of a protein is to mature and (optionally) dimerize
    def update_reactions(self, mixture, debug=False):
        assy = self.assy                    # Get DNA assembly we are part of
        parameters = assy.cds.parameters    # get parameter values

        if self.dimerize:
            #! Move to mechanism function?
            add_reaction(mixture, [self.protein, self.protein], [self.dimer],
                         kf = parameters['Dimerization_F'],
                         kr = parameters['Dimerization_R'])

        # Allow override of protein maturation time
        if self.maturation_time != None:
            parameters['Protein_Maturation'] = log(2)/(self.maturation_time)

        # Let the individual mechanisms create all of the reactions
        mechanisms = get_mechanisms(mixture, assy, self.mechanisms)
        mechanisms['maturation'].update_reactions(mixture, assy)
        
# Protein coding sequence (same as a CDS)
class ProteinCDS(CDS):
    "Protein coding sequence"

#
# Ctag subclasses
#
# The Ctag subclasses are used to C-terminus tags

class Ctag(DNA):
    #! TODO: add docstring
    "Ctag class - define C-terminus protein tag"
    def __init__(self, name, length=0, mechanisms={}, config_file=None,
                 parameters={}, **keywords):
        # DNA initialization
        DNA.__init__(self, name, length=length, mechanisms=mechanisms,
                     config_file=config_file, parameters=parameters,
                     prefix="ctag_", **keywords)

# Degradation tag
class DegradationTag(Ctag):
    #! TODO: add docstring
    def __init__(self, name, protease="ClpXP", length=9, mechanisms={},
                 config_file=None, parameters={}, **keywords):
        Ctag.__init__(self, name, length=length, mechanisms=mechanisms,
                      config_file=config_file, parameters=parameters,
                      **keywords)
        self.protease = protease

#
# UTR3 subclasses
#
# The UTR3 subclasses are used to create terminators.

class UTR3(DNA):
    "UTR3 class - define 3' untranslated region sequence"
    def __init__(self, name, length=0, mechanisms={}, config_file=None,
                 parameters={}, **keywords):
        # DNA initialization
        DNA.__init__(self, name, length=length, mechanisms=mechanisms, 
                     config_file=config_file, parameters=parameters, 
                     prefix="utr3_", **keywords)

# Terminator
class Terminator(UTR3):
    #! TODO: add docstring
    def __init__(self, name, length=50, mechanisms={}, config_file=None):
        UTR3.__init__(self, name, length, mechanisms, config_file,
                      prefix="term_")

#
# Functions for creatng and manipulating DNA
#

# Assemble fragments of DNA into a gene
def assemble_dna(
        prom, utr5, cds,        # required arguments
        ctag=None, utr3=None,   # optional positional arguments
        mechanisms = {},        # custom mechanisms 
        config_file = None,     # parameter configuration information
        parameters = {},        #   (overrides element defaults)
        name = None,            # component-specific arguments
        **keywords              # parameter keywords (passed to elements)
):
    # Create a new sequence of DNA
    sequence = DNAassembly(
        name, mechanisms=mechanisms, config_file=config_file,
        parameters=parameters, **keywords)

    # Initialize the name string if nothing was given
    if name == None: sequence.name = ""

    # Parse and store the promoter sequence
    if isinstance(prom, str):
        name, length = parse_DNA_string(prom)   # Get component name
        prom = load_model("Prom", name, length) # Load from library
        
    if isinstance(prom, Promoter):
        sequence.promoter = prom
        update_existing(prom.parameters, sequence.parameters)
        sequence.dnalength += prom.length
        if name == None: sequence.name += prom.name
    else:
        ValueError("invalid promoter specification")

    # Parse and store the 5' UTR
    if isinstance(utr5, str):
        name, length = parse_DNA_string(utr5)   # Get component name
        utr5 = load_model("UTR5", name, length) # Load from library

    if isinstance(utr5, UTR5):
        sequence.utr5 = utr5
        update_existing(utr5.parameters, sequence.parameters)
        sequence.dnalength += utr5.length
        sequence.rnalength += utr5.length
        if name == None: sequence.name += "--" + utr5.name
    else:
        ValueError("invalid UTR5 specification")

    # Parse and store the protein coding sequence
    if isinstance(cds, str):
        name, length = parse_DNA_string(cds)    # Get component name
        cds = load_model("CDS", name, length)  # Load from library

    if isinstance(cds, CDS):
        sequence.cds = cds
        update_existing(cds.parameters, sequence.parameters)
        sequence.dnalength += cds.length
        sequence.rnalength += cds.length
        sequence.peplength += cds.length
        if name == None: sequence.name += "--" + cds.name
    else:
        ValueError("invalid CDS specification")

    # Parse and store the C-terminus tag
    if isinstance(ctag, str):
        name, length = parse_DNA_string(ctag)   # Get component name
        ctag = load_model("Ctag", name, length) # Load from library

    if isinstance(ctag, Ctag):
        sequence.ctag = ctag
        update_existing(ctag.parameters, sequence.parameters)
        sequence.dnalength += ctag.length
        sequence.rnalength += ctag.length
        sequence.peplength += ctag.length
        if name == None: sequence.name += "--" + ctag.name
    else:
        ValueError("invalid Ctag specification")

    # Parse and store the 3' UTR
    if isinstance(utr3, str):
        name, length = parse_DNA_string(utr3)   # Get component name
        utr3 = load_model("UTR3", utr3, length) # Load from library
        
    if isinstance(utr3, UTR3):
        sequence.utr3 = utr3
        update_existing(utr3.parameters, sequence.parameters)
        sequence.dnalength += utr3.length
        sequence.rnalength += utr3.length
        if name == None: sequence.name += "--" + utr3.name
    else:
        ValueError("invalid UTR3 specification")

    return sequence

# Parse a DNA string (from the old MATLAB TX-TL modeling library)
def parse_DNA_string(spec):
    # First check to see if we have a name(length) specification
    m = re.search("^(\w+)\((\d+)\)$", spec)
    if m == None:
        # If not, see if we just find a name
        m = re.search("^(\w+)$", spec)
        if m != None:
            name = m.group(1)
            length = None
    else:
        name = m.group(1)
        length = int(m.group(2))

    # If we didn't get anything, generate an error
    if m == None:
        ValueError("Can't parse spec" + spec)

    # Return name and length as a tuple
    return name, length
