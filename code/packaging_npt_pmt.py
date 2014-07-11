import os
import simtk.openmm as mm
from simtk import unit as u

def write_file(filename, contents):
    with open(filename, 'w') as outfile:
        outfile.write(contents)

input_rundir = "./oldRUN0/"
output_rundir = "./RUN0/"

temperature = 300. * u.kelvin
nclones = 500

state = mm.XmlSerializer.deserialize(open(input_rundir + "/state0.xml").read())
integrator = mm.XmlSerializer.deserialize(open(input_rundir + "/integrator.xml").read())
system = mm.XmlSerializer.deserialize(open(input_rundir + "/system.xml").read())

context = mm.Context(system, integrator)
context.setState(state)


system_filename = os.path.join(output_rundir, "system.xml")
integrator_filename = os.path.join(output_rundir, "integrator.xml")

write_file(system_filename, mm.XmlSerializer.serialize(system))
write_file(integrator_filename, mm.XmlSerializer.serialize(integrator))

for clone_index in range(nclones):
    context.setVelocitiesToTemperature(temperature)
    state = context.getState(getPositions=True, getVelocities=True, getForces=True, getEnergy=True, getParameters=True, enforcePeriodicBox=True)
    state_filename = os.path.join(output_rundir, 'state%d.xml' % clone_index)
    serialized = mm.XmlSerializer.serialize(state)
    write_file(state_filename, serialized)
