from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u

code = "3DMV"
ff_name = "amber99sbnmr"
water_name = 'tip4p-fb'

which_forcefield = "%s.xml" % ff_name
which_water = '%s.xml' % water_name

pdb_filename = "./pdb_fixed/%s.pdb" % code
dcd_filename = "./equil_npt/%s_%s_%s.dcd" % (code, ff_name, water_name)
log_filename = "./equil_npt/%s_%s_%s.log" % (code, ff_name, water_name)

padding = 1.0 * u.nanometers
cutoff = 0.95 * u.nanometers
output_frequency = 1000
n_steps = 5000000

ff = app.ForceField(which_forcefield, which_water)

temperature = 300.
pressure = 1.0 * u.atmospheres

pdb = app.PDBFile(pdb_filename)

modeller = app.Modeller(pdb.topology, pdb.positions)
modeller.addSolvent(ff, padding=padding, model='tip4pew')

topology = modeller.topology
positions = modeller.positions

system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

integrator = mm.LangevinIntegrator(temperature, 1.0 / u.picoseconds, 1.0 * u.femtoseconds)
system.addForce(mm.MonteCarloBarostat(pressure, temperature, 25))
simulation = app.Simulation(topology, system, integrator)
simulation.context.setPositions(positions)
print('Minimizing...')
simulation.minimizeEnergy()

simulation.context.setVelocitiesToTemperature(temperature)
print('Equilibrating...')

simulation.reporters.append(app.DCDReporter(dcd_filename, output_frequency))
simulation.reporters.append(app.StateDataReporter(open(log_filename, 'w'), output_frequency, step=True, time=True, speed=True))
simulation.step(n_steps)
