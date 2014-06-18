import os
import mdtraj as md

storage_path = "/home/kyleb/dat/siegetank/"
trj0 = md.load("/home/kyleb/src/choderalab/FAHNVT/src/equil_npt/equil_npt_final_step.pdb")

path = os.path.join(storage_path, "c6bf09d3-4b24-424b-b550-5d08a526a0de/ff7921c4-7b1f-43fd-8c38-587cda5cd69a:vspg11/")
sorted_folders = sorted(os.listdir(path), key=lambda value: int(value))

trj = md.load([os.path.join(path, folder, "frames.xtc") for folder in sorted_folders], top=trj0)
trj.unitcell_lengths


trj = md.load(os.path.join(storage_path, "c6bf09d3-4b24-424b-b550-5d08a526a0de/ff7921c4-7b1f-43fd-8c38-587cda5cd69a:vspg11/1/frames.xtc"), top=trj0)
