import os
import mdtraj as md
import mdtraj.utils.fah

n_runs = 1
n_clones = 500  # To do: look this up via glob
project = 10466
codename = {10466:"T4", 10467:"src", 10468:"abl", 10469:"EGFR"}[project]

min_num_frames = 500
stride = 1

input_data_path = "/data/choderalab/fah/analysis/%d/concatenated_trajectories/" % project
output_data_path = "/data/choderalab/fah/analysis/%d/protein_trajectories/" % project
top_filename = "/data/choderalab/fah/analysis/FAHNVT/%s/equil_npt/equil_npt_final_step.pdb" % codename

trj0 = md.load(top_filename)
top, bonds = trj0.top.to_dataframe()
atom_indices = top.index[top.chainID == 0].values
trj0.restrict_atoms(atom_indices)
trj0.save(os.path.join(output_data_path, "../", "protein.pdb"))


for run in range(n_runs):
    for clone in range(n_clones):
        print(run, clone)
        in_filename = os.path.join(input_data_path, "run%d-clone%d.h5" % (run, clone))
        if not os.path.exists(in_filename):
            continue
        if len(md.formats.HDF5TrajectoryFile(in_filename)) < min_num_frames:
            continue
        trj = md.load(in_filename)[::stride]
        trj.restrict_atoms(atom_indices)
        out_filename = os.path.join(output_data_path, "run%d-clone%d.h5" % (run, clone))
        trj.save(out_filename)
