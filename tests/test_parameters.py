# Use default configuration information
ptet = txtl.models.ptet

# Create a new component with default configuration information
ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True)

# Overwrite system configuration file with local configuration file
ptet = txtl.RepressedPromoter('ptet', 'tetR', dimer=True,
                              config_file='prom_ptet.csv')
ptet = txtl.models.ptet('ptet.csv')

# Override a single parameter
bcd2 = txtl.ConstitutiveRBS('BCD2', Ribosome_Binding_F=10)
bcd2 = txtl.ConstitutiveRBS('BCD2', parameters = {Ribosome_Binding_F:10})

degfp = txtl.ProteinCDS('deGFP', maturation_time=30*txtl.minutes)

lva = txtl.DegradationTag('lva', 'clpXP')
