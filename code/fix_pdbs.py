import simtk.openmm.app as app
import pdbfixer

mutation_string = "GLY-112-ALA"
fixer = pdbfixer.PDBFixer(pdbid='2LCB')
fixer.applyMutations([mutation_string])
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.removeHeterogens(True)
fixer.addMissingHydrogens(7.0)
numChains = len(list(fixer.topology.chains()))
fixer.removeChains(range(1, numChains))
app.PDBFile.writeFile(fixer.topology, fixer.positions, open("./pdb_fixed/2LCB_%s.pdb" % mutation_string, 'w'))


fixer = pdbfixer.PDBFixer(pdbid='2LCB')
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.removeHeterogens(True)
fixer.addMissingHydrogens(7.0)
numChains = len(list(fixer.topology.chains()))
fixer.removeChains(range(1, numChains))
app.PDBFile.writeFile(fixer.topology, fixer.positions, open("./pdb_fixed/2LCB.pdb", 'w'))


mutation_string = "GLY-112-ALA"
fixer = pdbfixer.PDBFixer(pdbid='3DMV')
fixer.applyMutations([mutation_string])
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.removeHeterogens(True)
fixer.addMissingHydrogens(7.0)
numChains = len(list(fixer.topology.chains()))
fixer.removeChains(range(1, numChains))
app.PDBFile.writeFile(fixer.topology, fixer.positions, open("./pdb_fixed/3DMV_%s.pdb" % mutation_string, 'w'))


fixer = pdbfixer.PDBFixer(pdbid='3DMV')
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.removeHeterogens(True)
fixer.addMissingHydrogens(7.0)
numChains = len(list(fixer.topology.chains()))
fixer.removeChains(range(1, numChains))
app.PDBFile.writeFile(fixer.topology, fixer.positions, open("./pdb_fixed/3DMV.pdb", 'w'))
