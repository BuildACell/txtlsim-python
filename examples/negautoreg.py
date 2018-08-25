# negautoreg.m - negative autoregulation example
# R. M. Murray, 8 Sep 2012
#
# This file contains a simple example of setting up a TXTL simulation
# for a negatively autoregulated gene.  The constants for this example
# come from the Simbiology toolbox example page:
#
#    http://www.mathworks.com/help/toolbox/simbio/gs/fp58748.html
#

import txtl

tube1 = txtl.extract('E30VNPRL');
tube2 = txtl.buffer('E30VNPRL');
tube3 = txtl.create_mixture('negautoreg');

txtl.add_dna(tube3, 'ptet(50)', 'utr1(20)', 'tetR(1200)', 1, 'plasmid');
txtl.add_dna(tube3, 'ptet(50)', 'utr1(20)', 'deGFP(1000)', 1, 'plasmid');

mix = txtl.combine([tube1, tube2, tube3]);
txtl.addspecies(mix, 'aTc', 500);

# [simData] = txtl.runsim(Mobj,14*60*60);
# txtl.plot(simData,Mobj);
