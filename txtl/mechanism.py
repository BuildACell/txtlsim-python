# mechanism.py - mechanism class for implementing TX-TL mechanisms
# RMM, 16 Aug 2018
#
# Mechanisms the means by which all reactions in a TX-TL reaction are
# established.  Mechanisms can be overridden to allow specialized
# processing of core reactions (eg, adding additional detail, using
# simplified models, etc.
#
# Mechanisms are established in the following order (lower levels
# override higher levels):
#
# Default extract mechanisms
#   Default component mechanisms
#     Mechanisms passed to create_extract()
#       Mechanisms passed to Component()
#         Mechanisms based to Subcomponent() [eg, DNA elements]
#
# This hierarchy allows reactions to be created without the user
# having to specify any alternative mechanisms (defaults will be
# used), but also allows the user to override all mechanisms used for
# every component (e.g, by giving an alternative transcription
# mechanisms when setting up an extract) or individual mechanisms for
# a given component (by passing an alternative mechanism just to that
# component).
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

# Mechanism class for core mechanisms
class Mechanism:
    """Core mechanisms within a mixture (transcription, translation, etc)

    The Mechanism class is used to impelement different core
    mechanisms in TX-TL.  All specific core mechanisms should be
    derived from this class.

    """
    def __init__(self,name=''):
        self.name = name

    def update_species(self, mixture, component, conc): return None
    def update_reactions(self, mixture, component): return None

    def __str__(self):
        return self.name

# Utility function to retrieve mechanism list
def get_mechanisms(mixture, component, custom={}):
    mechanisms = {}                                 # initalize mechanism
    mechanisms.update(mixture.default_mechanisms)   # extract defaults
    mechanisms.update(component.default_mechanisms) # component defaults
    mechanisms.update(mixture.custom_mechanisms)    # customized extract
    mechanisms.update(component.custom_mechanisms)  # customized component 
    mechanisms.update(custom)                       # additional customization
    return mechanisms
