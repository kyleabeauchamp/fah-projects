import os
import glob
import mdtraj as md
from fahmunge import fah

target_id_map = {"NSD1_HUMAN_D0":"91f51e8a-7b40-4adc-8ca9-38786a9fe654", "SETD2_HUMAN_D0":"aa5325a2-2fec-46ac-a14a-ce1d46328a4c", "NSD2_HUMAN_D0":"23166b8f-dd82-408f-b1e8-b5657c67141c"}

for target, target_id in target_id_map.iteritems():
    storage_path = "/home/kyleb/dat/siegetank/"
    output_directory = "/home/kyleb/dat/siegetank_analysis/%s/" % target
    trj0 = md.load("/home/kyleb/src/choderalab/FAHNVT/%s/oldRUN0/system.pdb" % target)
    streams = glob.glob(os.path.join(storage_path, target_id, "*"))
    for stream in streams:
        output_filename = os.path.split(stream)[-1][0:25]
        output_filename = os.path.join(output_directory, output_filename + ".h5")
        fah.concatenate_ocore(stream, trj0, output_filename)
