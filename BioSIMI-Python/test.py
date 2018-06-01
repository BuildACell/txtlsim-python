from modules.utilityFunctions import *

plotSbmlWithBioscrape(['models/DP.xml','models/IFFL.xml'],0,np.linspace(0,10,100),[['inp','out'],['inp_IFFL','out_IFFL']])
# plotSbmlWithBioscrape('models/IFFL.xml',0,np.linspace(0,100,100),['inp_IFFL','out_IFFL'])
# plotSbmlWithBioscrape('models/DP.xml',0,np.linspace(0,100,100),['inp','out'])