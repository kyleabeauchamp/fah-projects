import os
import mdtraj as md
import mdtraj.utils.fah

n_runs = 1
n_clones = 500  # To do: look this up via glob
project = 10466
codename = {10466:"T4", 10467:"src", 10468:"abl", 10469:"EGFR"}[project]

input_data_path = "/data/choderalab/server.140.163.4.233/server2/data/SVR1401634233/PROJ%d/" % project
output_data_path = "/data/choderalab/fah/analysis/%d/concatenated_trajectories/" % project
top_filename = "/data/choderalab/fah/analysis/FAHNVT/%s/equil_npt/equil_npt_final_step.pdb" % codename

top = md.load(top_filename)

for run in range(n_runs):
    for clone in range(n_clones):
        print(run, clone)
        path = os.path.join(input_data_path, "RUN%d" % run, "CLONE%d" % clone)
        out_filename = os.path.join(output_data_path, "run%d-clone%d.h5" % (run, clone))
        print(path)
        print(out_filename)
        mdtraj.utils.fah.concatenate_core17(path, top, out_filename)
