
import json
import os

enemies = {}
path = 'Game/Gear'
for filename in os.listdir(path):
    file = '{}/{}'.format(path, filename)
    print(file)
    item = json.load(open(file, 'r+'))
    item['rarity'] = 0

    with open(file, 'w') as write_file:
        json.dump(item, write_file, indent=4)
