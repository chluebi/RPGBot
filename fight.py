from Data.Game import AI
from Data.Game import effects as ef
from Data.Game import abilities as abi_scripts
import os
from core import Tokens
from formatting import Battleembed as bembed
import formatting as form
from files import dict_to_obj


prefix = Tokens.prefix()


def load_abilities():
    abilitypath = 'Data/Game/Abilities/'
    abilitydata = {}
    for file in os.listdir(abilitypath):
        name, ext = os.path.splitext(file)
        abilitydata[name] = json.load(open(abilitypath + file))
    return abilitydata


AI.abidata = load_abilities()


def load_battles():
    battlepath = 'Data/Game/Battles/'
    data = {}
    datapure = {}
    for file in os.listdir(battlepath):
        folder, ext = os.path.splitext(file)
        path = os.path.join(battlepath, file)
        data[folder] = {}
        for file2 in os.listdir(path):
            name, ext = os.path.splitext(file2)
            jsonfile = json.load(open(os.path.join(path, file2)))
            data[folder][name] = jsonfile
            datapure[name] = jsonfile
    # print(data)
    return (data, datapure)


def load_enemies():
    enemypath = 'Data/Game/Enemies/'
    enemydata = {}
    for file in os.listdir(enemypath):
        name, ext = os.path.splitext(file)
        enemydata[name] = json.load(open(enemypath + file))
    return enemydata


abilitydata = load_abilities()
battledata = load_battles()
