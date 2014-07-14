import os
import glob
import mdtraj as md

target = "NSD1_HUMAN_D0"
target_id_map = {"NSD1_HUMAN_D0":"91f51e8a-7b40-4adc-8ca9-38786a9fe654"}
target_id = target_id_map[target]

storage_path = "/home/kyleb/dat/siegetank/"
output_directory = "/home/kyleb/dat/siegetank_analysis/%s/" % target

#trj0 = md.load("/home/kyleb/src/choderalab/FAHNVT/src/equil_npt/equil_npt_final_step.pdb")
trj0 = md.load("/home/kyleb/src/choderalab/FAHNVT/%s/oldRUN0/system.pdb" % target)

streams = glob.glob(os.path.join(storage_path, target_id, "*"))

for stream in streams:
    output_filename = os.path.split(stream)[-1][0:25]
    output_filename = os.path.join(output_directory, output_filename + ".h5")
    md.utils.fah.concatenate_ocore(stream, trj0, output_filename)
