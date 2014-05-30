import mdtraj as md
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u
from fah_parameters import *

#deviceid = 2
#platform = mm.Platform.getPlatformByName("CUDA")
#platform.setPropertyDefaultValue('CudaDeviceIndex', '%d' % deviceid) # select Cuda device index
platform = mm.Platform.getPlatformByName("OpenCL")

ff_name = "amber99sbildn"
water_name = 'tip3p'

which_forcefield = "%s.xml" % ff_name
which_water = '%s.xml' % water_name

pdb_filename = "./equil_npt/equil_npt.pdb"

out_pdb_filename = "./equil_nvt/equil_nvt.pdb"
dcd_filename = "./equil_nvt/equil_nvt.dcd"
log_filename = "./equil_nvt/equil_nvt.log"


ff = app.ForceField(which_forcefield, which_water)

pdb = app.PDBFile(pdb_filename)

topology = pdb.topology
positions = pdb.positions

system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

integrator = mm.LangevinIntegrator(temperature, friction, equil_timestep)
simulation = app.Simulation(topology, system, integrator, platform=platform)
simulation.context.setPositions(positions)
print('Minimizing...')
simulation.minimizeEnergy()

simulation.context.setVelocitiesToTemperature(temperature)
print('Equilibrating...')

simulation.reporters.append(app.DCDReporter(dcd_filename, output_frequency))
simulation.reporters.append(app.PDBReporter(out_pdb_filename, n_steps - 1))
simulation.reporters.append(app.StateDataReporter(open(log_filename, 'w'), output_frequency, step=True, time=True, speed=True))
simulation.step(n_steps)
