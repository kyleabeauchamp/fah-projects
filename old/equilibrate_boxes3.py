import os
import time
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u
import mdtraj.reporters
import sys

code = "3DMV"

ff_name = "amber99sbnmr"
water_name = 'tip3p'

which_forcefield = "%s.xml" % ff_name
which_water = '%s.xml' % water_name

platform_name = "CUDA"
timestep = 2.0 * u.femtoseconds
cutoff = 0.95 * u.nanometers
output_frequency = 5000
n_steps = 2500000
temperature = 300. 
pressure = 1.0 * u.atmospheres



pdb_filename = "./equil_box/%s.pdb" % code
dcd_filename = "./equil_box2/%s_%s.dcd" % (code, water_name)
log_filename = "./equil_box2/%s_%s.log" % (code, water_name)

traj = mdtraj.load(pdb_filename)
top, bonds = traj.top.to_dataframe()
atom_indices = top.index[top.chainID == 0].values

pdb = app.PDBFile(pdb_filename)
topology = pdb.topology
positions = pdb.positions

ff = app.ForceField(which_forcefield, which_water)

platform = mm.Platform.getPlatformByName(platform_name)

system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

integrator = mm.LangevinIntegrator(temperature, 1.0 / u.picoseconds, timestep)

simulation = app.Simulation(topology, system, integrator, platform=platform)
simulation.context.setPositions(positions)

system.addForce(mm.MonteCarloBarostat(pressure, temperature, 25))


simulation.minimizeEnergy()

simulation.context.setVelocitiesToTemperature(temperature)


print("Using platform %s" % simulation.context.getPlatform().getName())



simulation.reporters.append(mdtraj.reporters.DCDReporter(dcd_filename, output_frequency))
simulation.reporters.append(app.StateDataReporter(open(log_filename, 'w'), output_frequency, step=True, time=True, speed=True))
simulation.step(n_steps)
