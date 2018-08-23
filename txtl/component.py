# component.py - component class for implementing TX-TL components
# RMM, 16 Aug 2018
#
# This file defines the Component class that is used to create
# components of a TX-TL mixture.  The file is commented to serve as a
# template for creating a component.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .sbmlutil import add_species, add_reaction
from warnings import warn

# Component class for core components
class Component:
    """Component(name, mechanisms, config_file)

    The Component class is used to represent different components of a
    TX-TL mixture.  All specific components should be derived from
    this class.

    Data attributes
    ---------------
    name                Component name (str)
    mechanisms          Mechanism dictionary (dict)
    config_file         Configuration file (str)
    parameters          Parameter dictionary (dict)

    Required member functions
    -------------------------
    update_species()    create the species used by this component
    update_reactions()  create the reactions used by this component
    read_config_file()  read parameter values from configuration file
    write_config_file() write parametr value to configuration file

    """
    def __init__(self, name, mechanisms={}, config_file=None):
        """Component(name, [config_file], [mechanisms])

        Construct a component object.

        The default constructor for the Component object creates a
        component with a given name, which can be added to a TX-TL
        mixture.

        If the `config_file` argument is given, it specifies the name
        of a file that will be used to load parameter values that are
        specific to this component.  

        If the `mechanisms` argument is given, it specifies a
        dictionary of mechanisms that are used by component to create
        reactions.  The dictionary keys are component-specific, but
        should be documented so that they can be overriden by the
        user.  The dictionary values are Mechanism objects.

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
        self.mechanisms = {
            # 'mechanism' : MechanismConstructor()
        }

        # Add (or overwrite) any mechanisms passed as arguments
        self.mechanisms.update(mechanisms)

        # Read the configuration parameters
        self.parameters = {}
        if (config_file != None):
            self.parameters.update(load_config(config_file))

    #! TODO: think about argument order
    def update_species(self, model, mechanisms={}):
        """update_species(model, [mechanisms])

        Update (or create) the set of species associted with this component.

        The update_species() function is responsible for generating
        all of the species associated with this component, including
        any species that are needed by component-specific mechanisms.

        """
        # Create component specific species
        # self.product = add_species(model, "Type", name)
        
        # Create any other species needed by the transcriptional machinery
        for name in self.mechanisms:
            mechanisms[name].update_species(model, assy, mechanisms)
        
        # If the default member function gets used, issue a warning
        warn("component: default __init__ called for " + name)

    def update_reactions(self, model, mechanisms={}, parameters={}):
        """update_species(model, [mechanisms], [parameters])

        Update (or create) the set of reactions associated with this component

        The update_reactions() function is responsible for generating
        all of the reactions associated with this component, including
        any species that are needed by component-specific mechanisms.

        """
        # Create component specific species
        # self.product = add_species(model, "Type", name)

        # Create the parameter values for this reacton
        parameters.update(self.parameters)
        
        # Create any other species needed by the transcriptional machinery
        for name in self.mechanisms:
            mechanisms[name].update_reactions(model, assy, mechanisms,
                                              parameters)
        
        # If the default member function gets used, issue a warning
        warn("component: default __init__ called for " + name)
