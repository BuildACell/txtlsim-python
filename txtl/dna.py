# dna.py - DNA class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import re                      # use Python's regular expression library

# The main DNA class, used to represent a DNA fragment
class DNA:
    """DNA class

    The DNA class is used to represent a DNA sequence that has a given
    length.  Its main purpose is as the parent object for DNA
    fragments and DNA assemblies.

    Data attributes
    ---------------
    name        Name of the sequence (str)
    length      Length of the sequence (int)

    """
    def __init__(self, name, length=0):
        self.name = name
        self.length = length

# DNA assembly
class DNAassembly:
    """DNA assembly class

    The DNA assembly class is used to represent a DNA assembly,
    typically consisting of a promoter, a ribosome binding site (5'
    UTR), a protein coding sequence (CDS), an optional C-terminus tag
    (for protein degradation), and a terminator (3' UTR).  Subclasses
    can be used to create specialized types of DNA and predefined
    subclasses are available for promoters, RBSs, etc.

    Data attributes
    ---------------
    name        Name of the sequence (str)
    length      Length of the sequence (int)
    promoter    Promoter sequence (DNA)
    utr5        5' UTR (DNA)
    cds         Coding sequence (DNA) 
    ctag        C-terminus tag (DNA)
    utr3        3' UTR (DNA)

    Methods
    -------
    update_species()    create/update species associated with construct
    update_reactions()  create/update reactions associated with construct

    """
    def __init__(self, name, length=0, promoter=None, utr5=None,
                 cds=None, ctag=None, utr3=None):
        self.name = name
        self.length = length
        self.promoter = promoter
        self.utr5 = utr5
        self.cds = cds
        self.ctag = ctag
        self.utr3 = utr3

    # Create/update all of the species associated with this DNA assembly
    def update_species(self, model):
        # Create the DNA species
        self.dna = add_species(model, "DNA", self.name)

        # Create the mRNA species
        rnaname = self.utr5.name + "--" + self.cds.name;
        if (self.ctag != None): rnaname += "--" + self.ctag.name
        self.rna = add_species(model, "RNA", rnaname)

        # Add promoter-specific species
        self.promoter.update_species(model, self.dna, self.rna)

        # Create the protein species
        protname = self.cds.name;
        if (self.ctag != None): protname += "--" + self.ctag.name
        self.protein = add_species(model, "protein", self.cds.name)
                
        # Process any protein-specific additions
        try:
            self.cds.update_species(model)
        except:
            None
                
    def update_reactions(self, model):
        if isinstance(self.promoter, DNA):
            # Create reactions that initiate transcription
            self.promoter.update_reactions(model, self.dna, self.rna)
            
        if isinstance(self.utr5, DNA):
            # Create reactions that control translation
            self.utr5.update_reactions(model, self.rna, self.protein)
            
        if isinstance(self.cds, DNA):
            # Create reactions that convert RNA into proteins
            self.cds.update_reactions(model, self.rna, self.protein)

        if isinstance(self.ctag, DNA):
            # Create reactions that degrade proteins
            self.ctag.update_reactions(model, self.protein)
            
        if isinstance(self.utr3, DNA):
            # Create reactions that terminate transcription
            self.utr3.update_reactions(model, self.rna)

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
    def update_reactions(self, model, rna, dna): return None

# Constitute promoter
class ConstitutivePromoter(Promoter):
    #! TODO: add docstring
    def __init__(self, name, length=50, rnapname="RNAP70",
                 RNAPbound_F=20, RNAPbound_R=400):
        self.name = name
        self.length = length
        self.rnapname = rnapname
        self.RNAPbound_F = RNAPbound_F
        self.RNAPbound_R = RNAPbound_R

    def update_species(self, model, dna, rna):
        # Create the RNA polymerase
        self.rnap = add_species(model, None, self.rnapname)

        # Create RNA polymerase bound to DNA
        self.rnap_bound = add_species(model, None,
                                      self.rnapname + ":" + dna.name)

    def update_reactions(self, model, dna, rna):
        add_reactions(model, [self.rnap, dna], rna, 
                      kf=RNAPbound_F, kr=RNAbound_R)

# Repressed promoter
class RepressedPromoter(Promoter):
    #! TODO: add docstring
    def __init__(self, name, repressor, length=50, rnapname="RNAP70",
                 dimer=False, RNAPbound_F=20, RNAPbound_R=400,
                 DNAsequestration_F=25e-1, DNAsequestration_R=1.11e-4):
        self.name = name
        self.length = length
        self.RNAPbound_F = RNAPbound_F
        self.RNAPbound_R = RNAPbound_R
        self.DNAsequestration_F = DNAsequestration_F
        self.DNAsequestration_R = DNAsequestration_R
        self.tfname = repressor
        self.rnapname=rnapname
        self.dimer = dimer

    def update_species(self, model, dna, rna):
        # Create species for unrepressed promoter
        ConstitutivePromoter.update_species(self, model, dna, rna)

        # Create species for the transcription factor
        self.tf_species = add_species(model, "Protein", self.tfname)
        
        # Create repressor bound to DNA
        self.tf_bound = add_species(model, "Complex",
                                    self.tf_species.name + ":" + dna.name)

    def update_reactions(self, model, dna, rna):
        # Create reactios for unrepressed promoter
        Promoter.update_reactions(self, model, dna, rna)

        # Create sequestration reaction
        add_reaction(model, [self.tf_species, dna], [self.tf_bound],
                      kf=self.DNAsequestration_F, kr=self.DNAsequestration_R)

#
# UTR5 subclasses
#
# The UTR5 subclasses are used to create ribosome binding sites (RBSs).

class UTR5(DNA):
    "UTR5 class - define 5' untranslated region sequence"
    def update_reactions(self, model, rna, protein): return None

# Constitutive RBS
class ConstitutiveRBS(UTR5):
    #! TODO: add docstring
    def __init__(self, name, length=20,
                 Ribosome_Binding_F=0.2, Ribosome_Binding_R=4):
        UTR5.__init__(self, name, length)
        self.Ribosome_Binding_F = Ribosome_Binding_F
        self.Ribosome_Binding_R = Ribosome_Binding_R

#
# CDS subclasses
#
# The CDS subclasses are used to create proteins and peptides

class CDS(DNA):
    "CDS class - define protein coding sequence"
    def update_reactions(self, model, rna, protein): return None

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
    "Ctag class - define C-terminus protein tag"
    def update_reactions(self, model, protein): return None

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
    def update_reactions(self, model, rna): return None

# Terminator
class Terminator(UTR3):
    #! TODO: add docstring
    def __init__(self, name, length=50):
        UTR3.__init__(self, name, length)

#
# Functions for creatng and manipulating DNA
#

# Assemble fragmeents of DNA into a gene
def assemble_dna(prom, utr5, cds, ctag=None, utr3=None):
    # Create a new sequence of DNA
    sequence = DNAassembly("")

    # Parse and store the promoter sequence
    if isinstance(prom, str): prom = load_model("Prom", prom) 
    if isinstance(prom, Promoter):
        sequence.promoter = prom
        sequence.length += prom.length
        sequence.name += prom.name
    else:
        ValueError("invalid promoter specification")

    # Parse and store the 5' UTR
    if isinstance(utr5, str): utr5 = load_model("UTR5", utr5) 
    if isinstance(utr5, UTR5):
        sequence.utr5 = utr5
        sequence.length += utr5.length
        sequence.name += "--" + utr5.name
    else:
        ValueError("invalid UTR5 specification")

    # Parse and store the protein coding sequence
    if isinstance(cds, str): cds = load_model("Prot", cds) 
    if isinstance(cds, CDS):
        sequence.cds = cds
        sequence.length += cds.length
        sequence.name += "--" + cds.name
    else:
        ValueError("invalid CDS specification")

    # Parse and store the C-terminus tag
    if isinstance(ctag, str): ctag = load_model("Ctag", ctag) 
    if isinstance(ctag, Ctag):
        sequence.ctag = ctag
        sequence.length += ctag.length
        sequence.name += "--" + ctag.name
    else:
        ValueError("invalid Ctag specification")

    # Parse and store the 3' UTR
    if isinstance(utr3, str): utr3 = load_model("UTR3", utr3) 
    if isinstance(utr3, UTR3):
        sequence.utr3 = utr3
        sequence.length += utr3.length
        sequence.name += "--" + cds.name
    else:
        ValueError("invalid UTR3 specification")

    # Set the name of the DNA assembly

    return sequence

# Load a model from a file
#! TODO: move this to a better location
def load_model(prefix, spec):
    # Parse the string into a name and length
    name, length = parse_DNA_string(spec)

    # Look to see if we have a model for this promoter
    try:
        from importlib import import_module
        module = import_module("txtl.models.%s_%s" %
                               (prefix.lower(), name.lower()))
        model = eval("module.%s_%s('%s', %d)" %
                     (prefix, name.lower(), name, length))
    except:
        raise ValueError("couldn't find model %s_%s" % (prefix, name))

    return model

# Helper function to add a species to the model
#! TODO: move to a different location
def add_species(model, type, name):
    species = model.createSpecies()
    prefix = type + " " if type != None else ""
    species.setName(prefix + name)

    # Construct the species ID
    species_id = re.sub(" ", "_", prefix + name)
    species_id = re.sub("--", "_", species_id)
    species.setId(species_id)

    return species

# Helper function to add a reaction to a model
#! TODO: move to a different location
def add_reaction(model, reactants, products, kf, kr):
    reaction = model.createReaction()

    # Create the reactants
    for species in reactants:
        reactant = reaction.createReactant()
        reactant.setSpecies(species.getId())

    # Create the products
    for species in products:
        product = reaction.createProduct()
        product.setSpecies(species.getId())

    # Create the rate constants for forward and reverse reactions
    param = model.createParameter()
    param.setValue(kf)
    if (kr != None):
        reaction.setReversible(True)
        param = model.createParameter()
        param.setValue(kr)

    return reaction

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
