import os
import siegetank

storage_path = "/home/kyleb/dat/siegetank/"

my_token = os.environ["SIEGETANK_TOKEN"]
siegetank.login(my_token)

target_id_map = {"NSD1_HUMAN_D0":"91f51e8a-7b40-4adc-8ca9-38786a9fe654", "SETD2_HUMAN_D0":"aa5325a2-2fec-46ac-a14a-ce1d46328a4c", "NSD2_HUMAN_D0":"23166b8f-dd82-408f-b1e8-b5657c67141c"}
for target_str in target_id_map.values():
    target = siegetank.load_target(target_str)
    print(target)
    print(target.options)
    for stream in target.streams:
        print(stream.id)
        if stream.id == "d714ad9f-2dd4-4f24-b5a7-e2eec406f4f2:vspg11":  # There is a single corrupted stream that was previously causing issues
            continue
        data_folder = os.path.join(storage_path, target.id, stream.id)
        stream.sync(data_folder)
