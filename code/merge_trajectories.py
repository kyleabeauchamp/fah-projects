import os
import mdtraj as md
import mdtraj.utils.fah

n_runs = 1
n_clones = 500  # To do: look this up via glob

input_data_path = "/data/choderalab/server.140.163.4.233/server2/data/SVR1401634233/PROJ10466/"
output_data_path = "/data/choderalab/fah/analysis/10466/concatenated_trajectories/"
top_filename = "/data/choderalab/fah/analysis/FAHNVT/T4/equil_npt/equil_npt_final_step.pdb"

top = md.load(top_filename)

for run in range(n_runs):
    for clone in range(n_clones):
        print(run, clone)
        path = os.path.join(input_data_path, "RUN%d" % run, "CLONE%d" % clone)
        out_filename = os.path.join(output_data_path, "run%d-clone%d.h5" % (run, clone))
        print(path)
        print(out_filename)
        mdtraj.utils.fah.concatenate_core17(path, top, out_filename)
