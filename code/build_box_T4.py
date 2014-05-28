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

pdb_filename = "./pdb_fixed/%s.pdb" % code

out_pdb_filename = "./OLDRUN0/system.pdb"
dcd_filename = "./OLDRUN0/%s_%s_%s.dcd" % (code, ff_name, water_name)
log_filename = "./OLDRUN0/%s_%s_%s.log" % (code, ff_name, water_name)

ff = app.ForceField(which_forcefield, which_water)

pdb = app.PDBFile(pdb_filename)

modeller = app.Modeller(pdb.topology, pdb.positions)
modeller.addSolvent(ff, padding=padding, model='tip3p')

topology = modeller.topology
positions = modeller.positions

system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

integrator = mm.LangevinIntegrator(temperature, equil_friction, equil_timestep)
system.addForce(mm.MonteCarloBarostat(pressure, temperature, barostat_frequency))

platform = mm.Platform.getPlatformByName("CUDA")

simulation = app.Simulation(topology, system, integrator, platform=platform)
simulation.context.setPositions(positions)
print('Minimizing...')
simulation.minimizeEnergy()

simulation.context.setVelocitiesToTemperature(temperature)
print('Equilibrating...')

n_steps = 10000

simulation.reporters.append(app.PDBReporter(out_pdb_filename, n_steps - 1))
simulation.reporters.append(app.DCDReporter(dcd_filename, output_frequency))
simulation.step(n_steps)  # This system will be re-minimized and equilibrated later.

del simulation
del system
t = md.load(dcd_filename, top=out_pdb_filename)
t0 = t[-1]
t0.unitcell_lengths = t.unitcell_lengths[-1]
t0.save(out_pdb_filename)