import os
import time
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u

def write_file(filename, contents):
    with open(filename, 'w') as outfile:
        outfile.write(contents)

code = "3DMV"

ff_name = "amber99sbildn"
water_name = 'tip3p'

which_forcefield = "%s.xml" % ff_name
which_water = '%s.xml' % water_name

timestep = 2.0 * u.femtoseconds
cutoff = 0.95 * u.nanometers
temperature = 300. 
friction = 0.25 / u.picoseconds

rundir = "./RUNS/RUN0/"
nclones = 400

system_filename = os.path.join(rundir, "system.xml")
integrator_filename = os.path.join(rundir, "integrator.xml")

pdb_filename = "./equil_nvt/%s_%s_%s.pdb" % (code, ff_name, water_name)

pdb = app.PDBFile(pdb_filename)
topology = pdb.topology
positions = pdb.positions

ff = app.ForceField(which_forcefield, which_water)
system = ff.createSystem(topology, nonbondedMethod=app.PME, nonbondedCutoff=cutoff, constraints=app.HBonds)

for force in system.getForces():
    try:
        force.setUseDispersionCorrection(False)
    except AttributeError:
        pass

integrator = mm.LangevinIntegrator(temperature, friction, timestep)

simulation = app.Simulation(topology, system, integrator)
simulation.context.setPositions(positions)
simulation.context.setVelocitiesToTemperature(temperature)

write_file(system_filename, mm.XmlSerializer.serialize(system))
write_file(integrator_filename, mm.XmlSerializer.serialize(integrator))

for clone_index in range(nclones):
    simulation.context.setVelocitiesToTemperature(temperature)
    state = simulation.context.getState(getPositions=True, getVelocities=True, getForces=True, getEnergy=True, getParameters=True, enforcePeriodicBox=True)
    state_filename = os.path.join(rundir, 'state%d.xml' % clone_index)
    serialized = mm.XmlSerializer.serialize(state)
    #good_energy = 'PotentialEnergy="-385845.'
    #bad_energy = 'PotentialEnergy="-383031.'  # Taken from running FAH client.
    #serialized = serialized.replace(good_energy, bad_energy)
    write_file(state_filename, serialized)
