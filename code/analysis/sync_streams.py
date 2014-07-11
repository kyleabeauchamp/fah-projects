import os
import siegetank

storage_path = "/home/kyleb/dat/siegetank/"

my_token = os.environ["SIEGETANK_TOKEN"]
siegetank.login(my_token)

targets = siegetank.list_targets()
target = targets[-1]

for stream in target.streams:
    print(stream.id)
    if stream.id == "d714ad9f-2dd4-4f24-b5a7-e2eec406f4f2:vspg11":
        continue
    data_folder = os.path.join(storage_path, target.id, stream.id)
    stream.sync(data_folder)
