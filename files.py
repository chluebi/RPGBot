import json
import os
import core
from core import Parsing
from core import GET


def dict_to_obj(data, obj):
    for name, key in data.items():
        if isinstance(key, (list, tuple)):
            setattr(obj, name, [x if isinstance(x, dict) else x for x in key].copy())
        else:
            setattr(obj, name, key.copy() if isinstance(key, dict) else key)


class User:
    playerpath = 'Data/Players'
    standard_player = json.load(open('Data/Game/standard_player.json', 'r'))
    print(standard_player)

    def __init__(self, name, identifier):
        if not os.path.exists('{}/{}.json'.format(User.playerpath, name)):
            dict_to_obj(self.standard_player, self)
            self.name = str(name)
            self.id = identifier
            self.save_self()
        else:
            file = open('{}/{}.json'.format(User.playerpath, name), 'r')
            data = json.load(file)
            for key, value in self.standard_player.items():
                if key not in data:
                    data[key] = value

            for key in data.copy():
                if key not in self.standard_player:
                    data.pop(key)

            dict_to_obj(data, self)
            self.save_self()
        self.user = GET.clientuser(self.id)
        print(self.__dict__)

        core.users.append(self)

    @staticmethod
    def load_all():
        core.users = []
        users = []
        files = os.listdir(User.playerpath)
        for file in files:
            filename = os.path.basename(file).replace('.json', '')
            User(filename, None)

        for user in users:
            print(user.name)

        return users

    def save_self(self):
        file = self.__dict__
        print(file)
        filename = os.path.join(User.playerpath, '{}.json'.format(self.name))
        with open(filename, "w+") as write_file:
            json.dump(file, write_file, indent=4)

    def remove_self(self):
        filename = os.path.join(User.playerpath, '{}.json'.format(self.name))
        os.remove(filename)
        i = 0
        for user in core.users:
            if user.id == self.id:
                core.users.pop(i)
            i += 1

    def give_item(self, item, amount):
        items = [itemx[0] for itemx in self.inventory]
        amounts = [itemx[1] for itemx in self.inventory]
        if item not in items:
            self.inventory.append((item, amount))
        else:
            self.inventory[self.inventory.index(item)] += amount

    def give_item_bulk(self, items):
        for item, amount in items:
            self.give_item(item, amount)

    def give_ability(self, ability):
        if ability not in self.abilities:
            self.abilities.append(ability)
        else:
            print('player already has ability')

    def give_starter(self, chosen):
        if chosen in Parsing.classes:
            items = Parsing.classes[chosen]['starter_items']
            items = [(x, y) for x, y in items]
            self.give_item_bulk(items)
            for ability in Parsing.classes[chosen]['starter_abilities']:
                self.give_ability(ability)
        else:
            raise Exception('Class not found')


class Item:
    pass
