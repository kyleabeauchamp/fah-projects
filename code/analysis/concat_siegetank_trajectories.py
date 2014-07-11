import os
import glob
import mdtraj as md

storage_path = "/home/kyleb/dat/siegetank/"
output_directory = "/home/kyleb/dat/siegetank_analysis/src/"

target_id = "db01ac5c-5075-4401-a5df-797b846c1443"
trj0 = md.load("/home/kyleb/src/choderalab/FAHNVT/src/equil_npt/equil_npt_final_step.pdb")

streams = glob.glob(os.path.join(storage_path, target_id, "*"))

for stream in streams:
    output_filename =  os.path.split(stream)[-1][0:25]
    output_filename = os.path.join(output_directory, output_filename + ".h5")
    md.utils.fah.concatenate_ocore(stream, trj0, output_filename)
