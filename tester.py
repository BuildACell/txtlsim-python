from txtl.functions import *

tube = newtube("models/gene_expression_with_delay.xml")

add_dna(tube, 'ptet(50)', 'utr1(20)', 'tetR(1200)', 1, 'plasmid');
tube._add_species('mRNA')
print(tube.get_species_list())
