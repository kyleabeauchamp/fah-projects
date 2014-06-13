import os
import siegetank

storage_path = "/home/kyleb/dat/siegetank/"

my_token = os.environ["SIEGETANK_TOKEN"]
siegetank.login(my_token)

target = siegetank.list_targets()[-1]

for stream in target.streams:
    print(stream.id)
    data_folder = os.path.join(storage_path, target.id, stream.id)
    stream.sync(data_folder)
