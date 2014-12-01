import simtk.openmm.app as app
import pdbfixer

fixer = pdbfixer.PDBFixer(pdbid='4IJ8')
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.removeHeterogens(True)
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(7.0)
numChains = len(list(fixer.topology.chains()))
fixer.removeChains(range(1, numChains))
app.PDBFile.writeFile(fixer.topology, fixer.positions, open("./4IJ8_fixed.pdb", 'w'))
