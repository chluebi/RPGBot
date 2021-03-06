import json
import os
import core
from core import Parsing
from core import GET


def dict_to_obj(data, obj):
    for name, key in data.items():
        if isinstance(key, (list, tuple)):
            setattr(obj, name, [x.copy() if isinstance(x, dict) else x for x in key].copy())
        else:
            setattr(obj, name, key.copy() if isinstance(key, dict) else key)


def load_gear():
    gearpath = 'Data/Game/Gear/'
    geardata = {}
    for file in os.listdir(gearpath):
        name, ext = os.path.splitext(file)
        geardata[name] = json.load(open(gearpath + file))

    return geardata


geardata = load_gear()


class User:
    playerpath = 'Data/Players'
    standard_player = json.load(open('Data/Game/standard_player.json', 'r'))
    print(standard_player)

    def __init__(self, name, identifier):
        if not os.path.exists('{}/{}.json'.format(User.playerpath, name)):
            dict_to_obj(self.standard_player, self)
            self.abilities = []
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
            self.abilities = []
            self.stats = {}
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
        file_original = self.__dict__
        file = file_original.copy()
        file['user'] = 0
        file['stats'] = 0
        file['abilities'] = 0
        print(file)
        filename = os.path.join(User.playerpath, '{}.json'.format(self.name))
        with open(filename, "w+") as write_file:
            json.dump(file, write_file, indent=4)

        self.reload()

    def reload(self):
        self.stats = {}

        self.stats['strength'] = 10 + self.level * 2
        self.stats['intelligence'] = 10 + self.level * 2
        self.stats['defense'] = 10 + self.level * 2
        self.stats['magic_defense'] = 10 + self.level * 2
        self.stats['precision'] = 10 + self.level * 2

        self.health = 100 + self.level * 20
        self.abilities = []
        for pos, item in self.equipped.items():
            if item == 0:
                continue
            item = geardata[item]
            for stat, value in item['stats'].items():
                if stat == 'health':
                    self.health += value
                else:
                    self.stats[stat] += value

            for ability in item['abilities']:
                if ability not in self.abilities:
                    self.abilities.append(ability)

    def remove_self(self):
        filename = os.path.join(User.playerpath, '{}.json'.format(self.name))
        os.remove(filename)
        i = 0
        for user in core.users:
            if user.id == self.id:
                core.users.pop(i)
            i += 1

    async def give_item(self, item, amount):
        if item == 'xp':
            await self.give_xp(amount)
        else:
            if item not in self.inventory:
                self.inventory[item] = amount
            else:
                self.inventory[item] += amount

            if self.inventory[item] < 1:
                del self.inventory[item]
                return 'Removed ``{}`` of **{}**'.format(amount, item)

        return 'You have received ``{}`` of **{}**'.format(amount, item)

    async def give_item_bulk(self, items):
        endstring = ''
        for item, amount in items:
            endstring += await self.give_item(item, amount)
            endstring += '\n'

        return endstring

    async def give_ability(self, ability):
        if ability not in self.abilities:
            self.abilities.append(ability)
        else:
            print('player already has ability')

    async def give_starter(self, chosen):
        if chosen in Parsing.classes:
            items = Parsing.classes[chosen]['starter_items']
            items = [(x, y) for x, y in items]
            await self.give_item_bulk(items)
            for item, amount in items:
                self.equip(item)
            for ability in Parsing.classes[chosen]['starter_abilities']:
                await self.give_ability(ability)
        else:
            raise Exception('Class not found')

    async def give_xp(self, amount):
        self.xp += amount
        xplimit = ((self.level + 1) * 100)
        while self.xp > xplimit:
            await self.level_up()
            xplimit = ((self.level + 1) * 100)
            self.xp -= xplimit

    async def level_up(self):
        self.level += 1
        user = GET.clientuser(self.id)
        await user.send('You levelled up! New level {}'.format(self.level))
        self.reload()

    def equip(self, item):
        if not item in geardata:
            raise Exception('Item not found')

        self.equipped[geardata[item]['position']] = item

        self.save_self()

        return 'Equipped **{}**'.format(item)

    def unequip(self, item):
        if not item in [value for key, value in self.equipped.items()]:
            if not item in [key for key, value in self.equipped.items()]:
                return None
            else:
                if self.equipped[item] != 0:
                    temp = self.equipped[item]
                    self.equipped[item] = 0
                    return 'Unequipped **{} ({})**'.format(temp, item)
                else:
                    return 'No gear'

        self.equipped[geardata[item]['position']] = 0
        self.save_self()

        return 'Unequipped **{} ({})**'.format(item, geardata[item]['position'])


class Item:
    pass
