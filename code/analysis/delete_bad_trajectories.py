import tables
import glob
import os
import mdtraj as md
import mdtraj.utils.fah

n_runs = 1
n_clones = 500  # To do: look this up via glob
project = 10468
codename = {10466:"T4", 10467:"src", 10468:"abl", 10469:"EGFR"}[project]

input_data_path = "/data/choderalab/fah/analysis/%d/concatenated_trajectories/" % project

filenames = glob.glob(os.path.join(input_data_path, "run*-clone*.h5"))


for filename in filenames:
    file = tables.File(filename, 'r')
    if "coordinates" not in file.root:
        os.unlink(filename)
        print("deleted")
