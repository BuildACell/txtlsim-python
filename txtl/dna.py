# dna.py - DNA class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.
#
# This file contains the implementation of DNA in the txtlsim toolbox.
# This includes objects that represent the individual elements of a
# DNA assembly as well as the functions required to create the models
# associated with gene expression.

import re                      # use Python's regular expression library
from .component import Component
from .sbmlutil import add_species, add_reaction
from .mechanism import Mechanism
from .pathutil import load_model
from .config import load_config

# DNA assembly
class DNAassembly(Component):
    """DNA assembly class

    The DNA assembly class is used to represent a DNA assembly,
    typically consisting of a promoter, a ribosome binding site (5'
    UTR), a protein coding sequence (CDS), an optional C-terminus tag
    (for protein degradation), and a terminator (3' UTR).  Subclasses
    can be used to create specialized types of DNA and predefined
    subclasses are available for promoters, RBSs, etc.

    The DNA assembly follows the rules of a Component but it is more
    complex because each of the elements of the assembly
    (subcomponents) have their own functions.  As a consequence, most
    of what the assembly construct does is to keep track of the
    individual subcomponents and calls on those subcomponent to
    generate species and reactions.

    Data attributes
    ---------------
    name        Name of the sequence (str)
    length      Length of the sequence (int)
    promoter    Promoter sequence (DNA)
    utr5        5' UTR (DNA)
    cds         Coding sequence (DNA) 
    ctag        C-terminus tag (DNA)
    utr3        3' UTR (DNA)

    rnaname     Name of the RNA species (str)
    rnap        RNAP species (SMBLspecies)
    riboname    Name of the ribosome species (str)
    ribo        Ribosome species

    mechanisms  list of mechanisms for generating models

    Methods
    -------
    update_species()    create/update species associated with construct
    update_reactions()  create/update reactions associated with construct

    """
    def __init__(self, name, length=0, promoter=None, utr5=None,
                 cds=None, ctag=None, utr3=None, config_file=None,
                 mechanisms={}):
        self.name = name
        self.length = length
        self.promoter = promoter
        self.utr5 = utr5
        self.cds = cds
        self.ctag = ctag
        self.utr3 = utr3

        # Set up the default mechanisms
        self.mechanisms = {
            'maturation' : protein_maturation()
        }
        self.mechanisms.update(mechanisms)

        # Read the configuration parameters
        self.parameters = {}
        if (config_file != None):
            self.parameters.update(load_config(config_file))

    # Create/update all of the species associated with this DNA assembly
    def update_species(self, mixture, mechanisms, parameters={}, debug=False):
        model = mixture.model   # Get the model where we will store results
        
        # Create the DNA species
        self.dna = add_species(model, "DNA", self.name)

        # Let the individual DNA elements create the relevant species
        for dna in [self.promoter, self.utr5, self.cds,
                       self.ctag, self.utr3]:
            if dna != None:
                # Store the DNA assembly that generate this component
                dna.assy = self

                # Decide what mechanisms and parameters to pass to component
                #! TODO: need to figure out how to implement this
                
                # Update the species required for this component
                if debug: print("DNAassembly species update:", dna.name)
                dna.update_species(mixture, mechanisms,
                                   parameters=self.parameters)

    # Create/update all of the relevant reactions for this DNA assembly
    def update_reactions(self, mixture, default_mechanisms={},
                         parameters={}, debug=False):
        # Go through each subcomponent and update reactions
        for dna in [self.promoter, self.utr5, self.cds,
                       self.ctag, self.utr3]:
            if dna != None:
                # Sort out which mechanisms to use
                mechanisms = default_mechanisms         # model mechanisms
                mechanisms.update(self.mechanisms)      # assembly mechanisms
                mechanisms.update(dna.mechanisms)       # fragment mechanisms
                dna.update_reactions(mixture, mechanisms, parameters)
            
# The main DNA class, used to represent a DNA fragment
class DNA(Component):
    """DNA class

    The DNA class is used to represent a DNA sequence that has a given
    length.  Its main purpose is as the parent object for DNA
    fragments and DNA assemblies.

    Data attributes
    ---------------
    name        Name of the sequence (str)
    length      Length of the sequence (int)
    assy        DNA assembly that we are part of
    mechanisms  Local mechanisms for this component (overrides defaults)

    """
    def __init__(self, name, length=0, mechanisms={},
                 config_file=None, prefix="dna_"):
        self.name = name
        self.length = length
        self.mechanisms = mechanisms
        self.prefix = prefix

        # Read in parameters from the config file
        self.parameters = {}
        if config_file != None:
            self.parameters = load_config(prefix + name.lower())
            if self.parameters == None: self.parameters = {}

    # Set up default update functions to do nothing
    def update_species(self, mixture, mechanisms, parameters={}): return None
    def update_reactions(self, mixture, mechanisms, parameters={}): return None

#
# Promoter subclasses
#
# The promoter subclasses are used to create standard promoters
# (constitutive, repressed, activated).  When creating an instance of
# one of these subclasses, the name of the transcriptional regulator
# (if any) is passed as an argument and the appropriate reactions are
# instantiated.
# Promoter sequence

class Promoter(DNA):
    "Promoter class - define a promoter sequence"
    def __init__(self, name, length=50, config_file=None, rnapname="RNAP", 
                 RNAPbound_F='RNAPbound_F', RNAPbound_R='RNAPbound_R',
                 mechanisms={}):
        # Promoter initialization
        DNA.__init__(self, name, length, mechanisms, config_file,
                     prefix="prom_")

        # Set (or reset) values based on function arguments
        self.rnapname = rnapname
        self.RNAPbound_F = RNAPbound_F
        self.RNAPbound_R = RNAPbound_R

    def update_species(self, mixture, mechanisms, parameters={}):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of
        
        # Create the mRNA species
        assy.rnaname = assy.utr5.name + "--" + assy.cds.name
        if (assy.ctag != None): assy.rnaname += "--" + assy.ctag.name
        assy.rna = add_species(model, "RNA", assy.rnaname)

        # Create the RNA polymerase
        #! TODO: Does this belong here?  Not produced by the promoter
        assy.rnap = add_species(model, None, self.rnapname)

        # Create RNA polymerase bound to DNA
        assy.rnap_bound = add_species(model, "Complex",
                                      self.rnapname + ":" + assy.name)

        # Create any other species needed by the transcriptional machinery
        mechanisms['transcription'].update_species(mixture, assy, mechanisms,
                                                   parameters)
        
    # Default action of a promoter is to implement transcription
    def update_reactions(self, mixture, mechanisms, parameters={}, debug=False):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the parameter values for this reacton
        parameters.update(self.parameters)

        # Create the reactions required for transcription
        mechanisms['transcription'].update_reactions(mixture, assy, mechanisms,
                                                     parameters)

# Constitute promoter
class ConstitutivePromoter(Promoter):
    "ConstitutivePromoter - define a constitutive promoter"

# Repressed promoter
class RepressedPromoter(Promoter):
    #! TODO: add docstring
    def __init__(self, name, repressor, length=50, rnapname="RNAP",
                 dimer=False, 
                 RNAPbound_F='RNAPbound_F', RNAPbound_R='RNAPbound_R',
                 DNAsequestration_F=25e-1, DNAsequestration_R=1.11e-4,
                 mechanisms={}):
        # Promoter initialization
        Promoter.__init__(self, name, length, 
                          RNAPbound_F=RNAPbound_F, RNAPbound_R=RNAPbound_R,
                          mechanisms=mechanisms)
        self.DNAsequestration_F = DNAsequestration_F
        self.DNAsequestration_R = DNAsequestration_R
        self.tfname = repressor
        self.rnapname=rnapname
        self.dimer = dimer

    def update_species(self, mixture, mechanisms, parameters={}):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of

        # Create species for unrepressed promoter
        Promoter.update_species(self, model, mechanisms, parameters)

        # Create species for the transcription factor
        self.tf_species = add_species(model, "Protein", self.tfname)
        
        # Create repressor bound to DNA
        self.tf_bound = add_species(model, "Complex",
                                    self.tf_species.name + ":" + assy.name)

    def update_reactions(self, mixture, mechanisms, parameters={}, debug=False):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the reactions for the unbound promoter
        Promoter.update_reactions(self, mixture, mechanisms, parameters)
        if debug: print("-- RepressedPromoter done with Promoter reactions")

        # Create the reaction for the transcription factor binding to DNA
        add_reaction(model, [self.tf_species, assy.dna], [self.tf_bound],
                      kf=self.DNAsequestration_F, kr=self.DNAsequestration_R)

#
# UTR5 subclasses
#
# The UTR5 subclasses are used to create ribosome binding sites (RBSs).

class UTR5(DNA):
    "UTR5 class - define 5' untranslated region sequence"

# Constitutive RBS
class ConstitutiveRBS(UTR5):
    #! TODO: add docstring
    def __init__(self, name, length=20, riboname="Ribo",
                 Ribosome_Binding_F=0.2, Ribosome_Binding_R=4):
        UTR5.__init__(self, name, length)
        self.riboname = riboname

        #! TODO: read parameter values parameter file
        self.parameters = load_config("utr5_" + name.lower())
        if self.parameters == None: self.parameters = {}
        
        #! TODO: decide if these should be set here; I don't think so...
        self.Ribosome_Binding_F = Ribosome_Binding_F
        self.Ribosome_Binding_R = Ribosome_Binding_R

    def update_species(self, mixture, mechanisms, parameters={}):
        model = mixture.model   # Get the model where we will store results
        assy = self.assy        # Get the DNA assembly we are part of

        # Create the protein
        assy.protname = assy.cds.name
        if (assy.ctag != None): assy.protname += "--" + assy.ctag.name
        assy.protein = add_species(model, "Protein", assy.protname)

        # Create the ribosome
        #! TODO: think about whether this belongs here or not
        assy.ribo = add_species(model, None, self.riboname)

        # Create Ribosome bound to RNA
        assy.ribo_bound = add_species(model, "Complex",
                                      self.riboname + ":" + assy.rnaname)
        
        # Create any other species needed by the transcriptional machinery
        mechanisms['translation'].update_species(mixture, assy, mechanisms,
                                                 parameters)

    # Default action of a promoter is to implement transcription
    def update_reactions(self, mixture, mechanisms, parameters={}, debug=False):
        assy = self.assy        # Get the DNA assembly we are part of
        mechanisms['translation'].update_reactions(mixture, assy, mechanisms,
                                                   parameters)
        

#
# CDS subclasses
#
# The CDS subclasses are used to create proteins and peptides
#
#! Sort out whether we need anything more than CDS

class CDS(DNA):
    "CDS class - define protein coding sequence"
    def __init__(self, name, length=0, mechanisms={}):
        # Promoter initialization
        DNA.__init__(self, name, length, mechanisms)
        
        #! TODO: read parameter values parameter file
        self.parameters = load_config("cds_" + name.lower())
        if self.parameters == None: self.parameters = {}
        
    def update_species(self, mixture, mechanisms, parameters={}):
        model = mixture.model   # Get the model where we will store results
        
        # Create species for the protein
        add_species(model, "Protein", self.name)

    # Default action of a protein is to mature and (optionally) dimerize
    def update_reactions(self, mixture, mechanisms, parameters={}, debug=False):
        assy = self.assy        # Get the DNA assembly we are part of

        # Let the individual mechanisms create all of the reactions
        mechanisms['maturation'].update_reactions(mixture, assy, mechanisms,
                                                  parameters)

# Protein coding sequence
class ProteinCDS(CDS):
    #! TODO: add docstring
    def __init__(self, name, length=1000, maturation_time=None):
        CDS.__init__(self, name, length)

#
# Ctag subclasses
#
# The Ctag subclasses are used to C-terminus tags

class Ctag(DNA):
    #! TODO: add docstring
    "Ctag class - define C-terminus protein tag"

# Degradation tag
class DegradationTag(Ctag):
    #! TODO: add docstring
    def __init__(self, name, protease, length=10):
        Ctag.__init__(self, name, length)

#
# UTR3 subclasses
#
# The UTR3 subclasses are used to create terminators.

class UTR3(DNA):
    "UTR3 class - define 3' untranslated region sequence"

# Terminator
class Terminator(UTR3):
    #! TODO: add docstring
    def __init__(self, name, length=50):
        UTR3.__init__(self, name, length)

#
# Functions for creatng and manipulating DNA
#

# Assemble fragments of DNA into a gene
def assemble_dna(prom, utr5, cds, ctag=None, utr3=None):
    # Create a new sequence of DNA
    sequence = DNAassembly("")

    # Parse and store the promoter sequence
    if isinstance(prom, str):
        name, length = parse_DNA_string(prom)   # Get component name
        prom = load_model("Prom", name, length) # Load from library
        
    if isinstance(prom, Promoter):
        sequence.promoter = prom
        sequence.length += prom.length
        sequence.name += prom.name
    else:
        ValueError("invalid promoter specification")

    # Parse and store the 5' UTR
    if isinstance(utr5, str):
        name, length = parse_DNA_string(utr5)   # Get component name
        utr5 = load_model("UTR5", name, length) # Load from library

    if isinstance(utr5, UTR5):
        sequence.utr5 = utr5
        sequence.length += utr5.length
        sequence.name += "--" + utr5.name
    else:
        ValueError("invalid UTR5 specification")

    # Parse and store the protein coding sequence
    if isinstance(cds, str):
        name, length = parse_DNA_string(cds)    # Get component name
        cds = load_model("Prot", name, length)  # Load from library

    if isinstance(cds, CDS):
        sequence.cds = cds
        sequence.length += cds.length
        sequence.name += "--" + cds.name
    else:
        ValueError("invalid CDS specification")

    # Parse and store the C-terminus tag
    if isinstance(ctag, str):
        name, length = parse_DNA_string(ctag)   # Get component name
        ctag = load_model("Ctag", name, length) # Load from library

    if isinstance(ctag, Ctag):
        sequence.ctag = ctag
        sequence.length += ctag.length
        sequence.name += "--" + ctag.name
    else:
        ValueError("invalid Ctag specification")

    # Parse and store the 3' UTR
    if isinstance(utr3, str):
        name, length = parse_DNA_string(utr3)   # Get component name
        utr3 = load_model("UTR3", utr3, length) # Load from library
        
    if isinstance(utr3, UTR3):
        sequence.utr3 = utr3
        sequence.length += utr3.length
        sequence.name += "--" + cds.name
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

#
# Default core mechanisms for transcription and translation
#
# These functions define the core mechanisms used to implement
# transcription and translation of a DNA assembly.
#

#! TODO: move core mechanisms to mechanisms/ directory

# Convert DNA to RNA
class dna2rna_basic(Mechanism):
    "Basic transcription mechanism"
    def update_reactions(self, mixture, assy, mechanisms, parameters={},
                         debug=False):
        model = mixture.model   # Get the model where we will store results
        
        # Create reaction that binds RNAP to DNA
        add_reaction(model, [assy.rnap, assy.dna], [assy.rnap_bound], 
                     kf=assy.promoter.RNAPbound_F,
                     kr=assy.promoter.RNAPbound_R)

        # Create reaction that produces mRNA
        if debug: print("dna2rna_basic: produce mRNA")
        add_reaction(model, [assy.rnap_bound], [assy.rnap, assy.rna], kf=1)
        
class rna2prot_basic(Mechanism):
    "Basic translation mechanism"
    def update_reactions(self, mixture, assy, mechanisms, parameters={},
                         debug=False):
        model = mixture.model   # Get the model where we will store results

        # Create reaction that binds Ribo to RNA
        add_reaction(model, [assy.ribo, assy.rna], [assy.ribo_bound], 
                     kf=assy.utr5.Ribosome_Binding_F,
                     kr=assy.utr5.Ribosome_Binding_R)

        # Create reaction that produces protein
        if debug: print("dna2rna_basic: produce mRNA")
        add_reaction(model, [assy.ribo_bound], [assy.ribo, assy.protein], kf=1)

class protein_maturation(Mechanism):
    "Basic protein maturation"
    def update_reactions(self, mixture, assy, mechanisms, parameters={},
                         debug=False):
        #! TODO: See if this protein is subject to maturation
        #! TODO: Create maturation reaction
        return None
