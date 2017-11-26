from bioscrape.types import Model
from tube import Tube

def newtube(filename):
	tube = Tube(filename)
	return tube

def extract(filename):
	tube = newtube(filename)
	#TODO: add more functionality here
	return tube

#e.g. add_dna(tube3, 'ptet(50)', 'utr1(20)', 'tetR(1200)', 1, 'plasmid');
#varargin represents multiple parameters
def add_dna(tube, prom_spec, utr_spec, cds_spec, dna_amount, type, *varargin):
	"""
	constructs the species and reactions required for transcription, translation and degradation of DNA, mRNA and proteins
		in the TX-TL system.

	:param tube: (txtl_tube.Tube) tube model object
	:param prom_spec: (str) spec of the form 'pre_prom(nn)'-'prom(nn)' where 'prom' is the 
		promoter name and 'len' is the length of the promoter. 
		pre_prom could consist of nucleatide sequences and corresponding sizes. One example of their use is as a protection from exonucleases. 
	:param utr_spec: (str) spec of the form 'rbs(nn)' where 'rbs' is the RBS
		name and 'len' is the length of the RBS.
	:param cds_spec: (str) spec of the form 'gene(nn)-lva(nn)-terminator(nn)' where 'gene' is the
		gene name and 'len' is the length of the gene.
	:param dna_amount: (int) amount of DNA to put in the tube (in nM)
	:param type: (str) 'linear' if you want to include degradation reactions
	:return: None
	"""
	if not varargin:
		#no extra arguments
		pass

	#store variations in DNA
	mode = {'add_dna_driver' : [],
			  'prot_deg_flag': False,
			  'no_protein_flag': False, 
			  'prot_term_flag': False,
			  'prom_junk_flag': False,
			  'prom_thio_flag': False}

	promData, promStr = parsespec(prom_spec)
	utrData, utrStr = parsespec(utr_spec)
	geneData, geneStr = parsespec(cds_spec)

	#check for variations in DNA, used to select specific code
	mode["prot_deg_flag"] = 'lva' in geneData[0]
	mode["no_protein_flag"] = 'no_protein' in geneData[0]
	mode["prot_term_flag"] = 'terminator' in geneData[0]
	mode["prom_junk_flag"] = 'junk' in promData[0]
	mode["prom_thio_flag"] = 'thio' in promData[0]
	
	#species name string building
	geneName = geneData[0]; #assuming the format is gene-lva-...-terminator
	rbsName = utrData[0]; #format is att-...-rbs.

	protstr = 'protein ' + geneStr #protstr looks something like 'protein tetR-lva-terminator'
	if mode['no_protein_flag']:
		rnastr = 'RNA ' + utrStr
		dnastr = 'DNA ' + promStr + '--' + utrStr
	else:
		rnastr = 'RNA ' + utrStr + '--' + geneStr
		dnastr = 'DNA ' + promStr + '--' + utrStr + '--' + geneStr

	promoterName = promData[0] # assuming {'thio','junk','prom'}


	printer(rnastr, dnastr, promoterName)

def addspecies(tube, name, amount, *varargin):
	tube.__add__species(name)

def parsespec(spec):
	"""
	Utility function for parsing out a specification string
	
	:param spec: (str) specification in format str(data) e.g. ptet(50)
	:return (parsedData, combinedStr): data, str e.g. 'ptet(50)' --> (('ptet', 50), 'ptet')
	"""
	if len(spec) < 1:
		raise Exception('spec len < 1')
	parsedData = spec[spec.index("(") + 1:spec.rindex(")")]
	combinedStr = spec[:spec.index("(")]
	return ([combinedStr, parsedData], combinedStr)

def printer(*args):
	"""
	Tester function to print variable values more easily
	takes in variable number of variables and prints them in a list
	"""
	print '[',
	for arg in args:
		print str(arg) + ', ',
	print(']')






