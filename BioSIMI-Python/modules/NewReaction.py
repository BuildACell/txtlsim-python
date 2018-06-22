from libsbml import *
import re

class NewReaction(object):
    """
        Attributes:
            Reaction: A Reaction object   
    """

    def __init__(self, Reaction):
        self.Reaction = Reaction

    def getReaction(self):
        '''Returns the Reaction object '''
        return self.Reaction

    def setReaction(self, reaction):
        '''The Reaction object attribute is set '''
        self.Reaction = reaction

    def parseReactionString(self, rStr):
        '''
        Parses the reaction string to return a list of reactants (and products), a list of 
        stoichiometry constants of the reactants (and products)
        '''
        rxn = self.getReaction()
        if '-->' in rStr:
            rReversible = False
        elif '<->' in  rStr:
            rReversible = True

        check(rxn.setReversible(rReversible), 'set r_obj reversible')
        if not rxn.isSetReversible():
           raise SyntaxError('Reaction reversible attribute is not set.')

        rStr = rStr.replace(' ', '')
        if rxn.getReversible():
            s_rxn = rStr.split('<->')
        else:
            s_rxn = rStr.split('-->')

        if len(s_rxn) != 2:
            raise SyntaxError('Reaction string should have one arrow only')

        s_reac = s_rxn[0]
        s_pro = s_rxn[1]

        reactants = s_reac.split('+')
        products = s_pro.split('+')
        reactant_stoichList = []
        reactantList = []
        for reactant in reactants:
            stoich = re.findall(r'\d+',reactant)
            if len(stoich) > 1:
                raise SyntaxError('Reaction string syntax not correct')
            if stoich == []:
                stoich_int = 1
                reactant_stoichList.append(stoich_int)
                reactantList.append(reactant)
            else:
                stoich_int = int(stoich[0])
                reactant_stoichList.append(stoich_int)
                reactantList.append(reactant.replace(stoich[0],''))

        product_stoichList = []
        productList = []
        for product in products:
            stoich = re.findall(r'\d+',product)
            if len(stoich) > 1:
                raise SyntaxError('Reaction string syntax not correct')
            if stoich == []:
                stoich_int = 1
                product_stoichList.append(stoich_int)
                productList.append(product)
            else:
                stoich_int = int(stoich[0])
                product_stoichList.append(stoich_int)
                productList.append(product.replace(stoich[0],''))

        return reactantList, reactant_stoichList, productList, product_stoichList


    def createNewReactant(self, rtSpeciesId, rtConstant, rtStoichiometry):
        '''
        Creates a new Reactant inside the current Reaction object and returns the
        SpeciesReference object to it
        '''
        species_ref_obj_reactant = self.getReaction().createReactant()
        check(species_ref_obj_reactant,
              'created species_ref_obj_reactant reactant')
        check(species_ref_obj_reactant.setSpecies(
            rtSpeciesId), 'set species_ref_obj_reactant ID')
        check(species_ref_obj_reactant.setConstant(rtConstant),
              'set species_ref_obj_reactant constant')
        check(species_ref_obj_reactant.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_reactant stoichiometry')
        return species_ref_obj_reactant

    def createNewProduct(self, rtSpeciesId, rtConstant, rtStoichiometry):
        '''
        Creates a new Product inside the current Reaction object and returns the
        SpeciesReference object to it
        '''
        species_ref_obj_product = self.getReaction().createProduct()
        check(species_ref_obj_product, 'created species_ref_obj_product produc')
        check(species_ref_obj_product.setSpecies(rtSpeciesId), 'set species_ref_obj_product ID')
        check(species_ref_obj_product.setConstant(rtConstant),
              'set species_ref_obj_product constant')
        check(species_ref_obj_product.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_product stoichiometry')
        return species_ref_obj_product

    def createRate(self, math_ast):
        '''
        Creates a new KineticLaw object inside the current Reaction and returns it.
        The AST_Node object given as an argument in 
        math_ast is used to define the rate 
        '''
        kinetic_law_reaction = self.getReaction().createKineticLaw()
        check(kinetic_law_reaction, 'create kinetic law')
        check(kinetic_law_reaction.setMath(math_ast), 'set math on kinetic law')
        return kinetic_law_reaction


    def createMath(self, formulaString):
        ''' 
        Creates a new math AST_Node using the formulaString given and returns it 
        '''
        math_ast = parseL3Formula(formulaString)
        check(math_ast, 'create AST for rate expression')
        return math_ast

def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value == None:
            raise SystemExit(
                'LibSBML returned a null value trying to ' + message + '.')
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        else:
            err_msg = 'Error encountered trying to ' + message + '.' \
                + 'LibSBML returned error code ' + str(value) + ': "' \
                + OperationReturnValue_toString(value).strip() + '"'
            raise SystemExit(err_msg)
    else:
        return

