# component.py - component class for implementing TX-TL components
# RMM, 16 Aug 2018
#
# This file defines the Component class that is used to create
# components of a TX-TL mixture.  The file is commented to serve as a
# template for creating a component.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.
"""
Components
----------

General documentation about components (TODO).
"""

from warnings import warn
from .sbmlutil import add_species, add_reaction
from .mechanism import get_mechanisms
from .parameter import eval_parameter

# Component class for core components
class Component:
    """Individual components within a TX-TL mixture

    The Component class is used to represent different components of a
    TX-TL mixture.  All specific components should be derived from
    this class.

    Data attributes
    ---------------
    name                Component name (str)
    default_mechanisms  Default mechanisms for the component (dict)
    custom_mechanisms   User-specified mechanisms for the component (dict)
    config_file         Name of the configuration file for parameter values
    parameters          Parameter dictionary (dict)

    Required member functions
    -------------------------
    update_species()    create the species used by this component
    update_reactions()  create the reactions used by this component

    Optional member functions [TODO: not implemented]
    -------------------------
    read_config_file()  read parameter values from configuration file
    write_config_file() write parametr value to configuration file

    """
    def __init__(self, name,
                 # expected_arg = default_val       # expected arguments
                 mechanisms={},                     # custom mechanisms
                 config_file=None, parameters={},   # parameter configuration
                 # additional_arg = default_val     # component-specific args
                 **keywords                         # parameter keywords
    ):
        """Construct a component object.

        The default constructor for the Component object creates a
        component with a given name, which can be added to a TX-TL
        mixture.

        If the `mechanisms` argument is given, it specifies a
        dictionary of mechanisms that are used by component to create
        reactions.  The dictionary keys are component-specific, but
        should be documented so that they can be overriden by the
        user.  The dictionary values are Mechanism objects.

        If the `config_file` argument is given, it specifies the name
        of a file that will be used to load parameter values that are
        specific to this component.  Individual parameters can be
        overridden using the `parameters` dictionary argument.

        """
        # Call the class constructor to get default argument processing
        # Component.__init__(self, name, config_file, mechanisms)
        
        # Set up the default mechanisms for this class
        #
        # Mechanisms that are specific to this component can be
        # contained in the file defining the mechanism.  More generic
        # mechanisms that may be used by multiople component types
        # should be placed in the mechanisms/ diretory and imported
        # before use.
        #
        self.default_mechanisms = {
            # 'mechanism' : MechanismConstructor()
        }

        # Add (or overwrite) any mechanisms passed as arguments
        self.custom_mechanisms = mechanisms

        # Create the config_file name (optional)
        if config_file == None:
            config_file = self.name.tolower() + ".csv"
        self.config_file = config_file
        
        # Set the component parameter values
        self.default_parameters = {
            # 'parameter' : value
        }
        self.parameters = get_parameters(
            config_file, parameters, self.default_parameters, **keywords)

        # Fill in any missing values for default parameters
        # Alternative setup for setting parameter values
        #

    # Define update_parameters to do nothing (overriden by extracts)
    def update_parameters(self, mixture):
        "Update (or create) (global) parameters in the model"

    #! TODO: think about argument order
    def update_species(self, mixture, concentration):
        """Update (or create) the set of species associated with this
        component.

        The update_species() function is responsible for generating
        all of the species associated with this component, including
        any species that are needed by component-specific mechanisms.

        """
        # Create component specific species
        # self.product = add_species(model, "Type", name)
        
        # Create any other species needed by component mechanisms
        mechanisms = get_mechanisms(mixture, self)
        for name in mechanisms:
            mechanism = mechanisms[name]
            mechanism.update_species(mixture, self, concentration)
        
        # If the default member function gets used, issue a warning
        warn("component: default __init__ called for " + name)

    def update_reactions(self, mixture):
        """Update (or create) the set of reactions associated with this
        component

        The update_reactions() function is responsible for generating
        all of the reactions associated with this component, including
        any species that are needed by component-specific mechanisms.

        """
        # Create component specific species
        # self.product = add_species(model, "Type", name)

        # Create the parameter values for this reacton
        parameters = parameters.copy()
        parameters.update(self.parameters)
        
        # Create any other reactions needed by component mechanisms
        mechanisms = get_mechanisms(mixture, component)
        for name in mechanisms:
            mechanism = mechanisms[name]
            mechanism.update_reactions(mixture, component)
        
        # If the default member function gets used, issue a warning
        warn("component: default __init__ called for " + name)

    def eval_parameter(self, name):
        return eval_parameter(self, name)
