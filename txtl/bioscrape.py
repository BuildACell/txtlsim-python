# bioscrape.py - interface to BioSCRAPE
# RMM, 27 Aug 2018 (based on BioSIMI code from Ayush Pandey)

import bioscrape
import numpy as np
import matplotlib.pyplot as plt

def runsim(
    mixture, duration, npts=1000,       # Required parameters
    filename='bioscrape.xml', t0=0      # Bioscrape customization
):
    # Create an SBML file for bioscrape to read
    mixture.write_sbml(filename)

    # Create the time vector
    timepoints = np.linspace(t0, duration, npts)

    # Run the simulator
    m = bioscrape.types.read_model_from_sbml(filename)
    s = bioscrape.simulator.ModelCSimInterface(m)
    s.py_prep_deterministic_simulation()
    s.py_set_initial_time(t0)
    sim = bioscrape.simulator.DeterministicSimulator()
    result = sim.py_simulate(s, timepoints)

    return (m, timepoints, result)

def plot(simdata, mixture, species_ids):
    model = mixture.model               # Get the SBML model
    (m, timepoints, result) = simdata   # Get BioSCRAPE results

    for id in species_ids:
        index = m.get_species_index(id)
        plt.plot(timepoints/60, result.py_get_result()[:, index])

    plt.legend(species_ids)
    plt.xlabel("Time [min]")
    plt.ylabel("Concentration [nM]")
    plt.show(block=False)
