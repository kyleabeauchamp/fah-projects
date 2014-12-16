import numpy as np
from fah_parameters import *
import simtk.openmm.app as app
import pdbfixer
import mdtraj as md

PADDING = 0.8 * u.nanometers

def fix(pdbid, padding=PADDING):
    fixer = pdbfixer.PDBFixer(pdbid=pdbid)
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.removeHeterogens(True)
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.0)
    numChains = len(list(fixer.topology.chains()))
    fixer.removeChains(range(1, numChains))
    file_handle = open("%s_fixed.pdb" % pdbid, 'wb')
    app.PDBFile.writeFile(fixer.topology, fixer.positions, file_handle)
    file_handle.close()

    ff_name = "amber99sbildn"
    water_name = 'tip3p'

    which_forcefield = "%s.xml" % ff_name
    which_water = '%s.xml' % water_name

    out_pdb_filename = "./equil/equil.pdb"
    ff = app.ForceField(which_forcefield, which_water)

    modeller = app.Modeller(fixer.topology, fixer.positions)
    modeller.addSolvent(ff, padding=padding)

    app.PDBFile.writeFile(modeller.topology, modeller.positions, open("./%s_box.pdb" % pdbid, 'w'))

fix("1ZKK")
fix("4IJ8")

# NOTE: this relies on the fact that waters are placed last.

pdbids = ["1ZKK", "4IJ8"]
trajectories = [md.load("./%s_box.pdb" % pdbid) for pdbid in pdbids]
n_atoms = min([t.n_atoms for t in trajectories])

for k, t in enumerate(trajectories):
    pdbid = pdbids[k]
    t.atom_slice(np.arange(n_atoms)).save("./%s_box.pdb" % pdbid)
