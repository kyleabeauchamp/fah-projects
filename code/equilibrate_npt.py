import mdtraj as md
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u
from fah_parameters import *

code = "3DMV"
ff_name = "amber99sbildn"
water_name = 'tip3p'

which_forcefield = "%s.xml" % ff_name
which_water = '%s.xml' % water_name

pdb_filename = "./OLDRUN0/system.pdb"

out_pdb_filename = "./equil_npt/%s_%s_%s.pdb" % (code, ff_name, water_name)
dcd_filename = "./equil_npt/%s_%s_%s.dcd" % (code, ff_name, water_name)
log_filename = "./equil_npt/%s_%s_%s.log" % (code, ff_name, water_name)


ff = app.ForceField(which_forcefield, which_water)

pdb = app.PDBFile(pdb_filename)

topology = pdb.topology
positions = pdb.positions

system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

integrator = mm.LangevinIntegrator(temperature, friction, equil_timestep)
system.addForce(mm.MonteCarloBarostat(pressure, temperature, barostat_frequency))
simulation = app.Simulation(topology, system, integrator)
simulation.context.setPositions(positions)
print('Minimizing...')
simulation.minimizeEnergy()

simulation.context.setVelocitiesToTemperature(temperature)
print('Equilibrating...')

simulation.step(discard_steps)  # Don't even save the first 25 ps

simulation.reporters.append(app.DCDReporter(dcd_filename, output_frequency))
simulation.reporters.append(app.PDBReporter(out_pdb_filename, n_steps - 1))
simulation.reporters.append(app.StateDataReporter(open(log_filename, 'w'), output_frequency, step=True, time=True, speed=True))
simulation.step(n_steps)

del simulation
del system
t = md.load(dcd_filename, top=out_pdb_filename)
t0 = t[-1]
t0.unitcell_lengths = t.unitcell_lengths.mean(0)
t0.save(out_pdb_filename)
