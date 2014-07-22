import numpy as np
import os
import glob
import mdtraj as md

min_traj_length = 100
trj0 = md.load("system.subset.pdb")
filenames = glob.glob("full_Trajectories/*.h5")

for in_filename in filenames:
    print(in_filename)
    out_filename = os.path.join("./Trajectories/", os.path.split(in_filename)[1])
    trj = md.load(in_filename, atom_indices=np.arange(trj0.n_atoms))
    if len(trj) > min_traj_length:
        trj.save(out_filename)
