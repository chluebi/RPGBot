import json
import core
import random
import asyncio
import random
import os
from files import dict_to_obj
from formatting import Battleembed as bembed
import formatting as form
from core import Tokens

from Data.Game import AI
from Data.Game import effects as ef

prefix = Tokens.prefix()


def load_abilities():
    abilitypath = 'Data/Game/Abilities/'
    abilitydata = {}
    for file in os.listdir(abilitypath):
        name, ext = os.path.splitext(file)
        abilitydata[name] = json.load(open(abilitypath + file))
    return abilitydata


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
    print(data)
    return (data, datapure)


def load_enemies():
    enemypath = 'Data/Game/Enemies/'
    enemydata = {}
    for file in os.listdir(enemypath):
        name, ext = os.path.splitext(file)
        enemydata[name] = json.load(open(enemypath + file))
    return enemydata


abilitydata = load_abilities()


async def new_battle(par, msg, player):
    data = load_battles()

    if player.status[0] == 'battle':
        await msg.channel.send('You already are in a battle!')
        return

    if len(par) < 2:
        msg.channel.send('Specify a battle! More info at with {}info battle'.format(prefix))
        return

    if par[1] == 'tutorial':
        await Battles.start_battle('tutorial', player, msg.channel)
        return

    if par[1] in ['c', 'cave', 'cavelands']:
        await Battles.start_battle('Cavelands', player, msg.channel)
        return

    await Battles.start_battle(par[1], player, msg.channel)


class Battles:
    data_original = load_battles()[0]
    datapure = load_battles()[1]

    @staticmethod
    async def start_battle(name, player, cha):
        data = Battles.data_original.copy()
        datapure = Battles.datapure.copy()
        chosen = name

        if chosen in data:
            battlelist = []
            for key, value in data[chosen].items():
                if value['min_level'] <= player.level and value['min_level'] + 3 > player.level:
                    for i in range(value['rarity']):
                        battlelist.append(key)
            print(battlelist)
            chosen = random.choice(battlelist)
            print(chosen)

        if chosen in datapure:
            if datapure[chosen]['min_level'] > player.level:
                cha.send('Your level is too low.')
            else:
                battledata = datapure[chosen]
        else:
            raise Exception('Battle not found')
        battle = Battle(battledata, player, cha)
        core.battles.append(battle)
        await battle.wait_for_player(cha)

    @staticmethod
    def available_battles(player):
        data = Battles.data_original.copy()
        battlelist = ''
        for folder, content in data.items():
            battlelist += '**{}**\n'.format(folder)
            for key, value in content.items():
                if value['min_level'] <= player.level and value['min_level'] + 3 > player.level:
                    battlelist += '- {} \n'.format(key)
            battlelist += '\n\n'

        return battlelist

    @staticmethod
    def battle_info(battle):
        battle = battle
        datapure = Battles.datapure
        if battle not in datapure:
            return None

        data = datapure[battle]
        desc = json.dumps(data)
        return form.basic(battle, desc)


class Battle:

    def __init__(self, data, player, cha):
        rand = -1
        usedrands = [battle.id for battle in core.battles]
        while rand in usedrands or rand == -1:
            rand = random.randint(0, 1000)
        self.data = data
        self.id = rand
        self.side1 = [Player(player)]
        self.channel = cha
        self.end = False
        self.message = []
        player.status = ['battle', self.id]
        print(player.__dict__)
        self.side2 = [Enemy(enemytype, level) for enemytype, level in data['enemies']]
        names = []
        amount = []
        # no dupe names
        for character in self.side2:
            if character.name not in names:
                names.append(character.name)
                amount.append(1)
                character.name = character.name + '1'
            else:
                index = names.index(character.name)
                character.name = character.name + str((amount[index] + 1))
                amount[index] = amount[index] + 1

        names = []
        amount = []
        for character in self.side1:
            if character.name not in names:
                names.append(character.name)
                amount.append(1)
                character.name = character.name
            elif character.name in names and amount[index(character.name)] == 1:
                character.name = character.name + 2
                amount[index] = amount[index] + 1
            else:
                index = names.index(character.name)
                character.name = character.name + str((amount[index] + 1))
                amount[index] = amount[index] + 1

        # scaling
        for character in self.side2:
            stats = character.stats
            for key, value in stats.items():
                stats[key] = value[0] + value[1] * character.level

        # set index and side
        for i, char in enumerate(self.side1):
            char.side = 1
            char.index = i
        for i, char in enumerate(self.side2):
            char.side = 2
            char.index = i

        self.turn = 1
        print(self.__dict__)

    def remove_self(self):
        players = [player for player in self.side1 if player.isplayer == True]
        players += [player for player in self.side2 if player.isplayer == True]

        for player in players:
            leaver = core.GET.player(player.id)
            leaver.status = ['None']
            leaver.save_self()
        i = 0
        for battle in core.battles:
            if battle.id == self.id:
                core.battles.pop(i)
            i += 1

    @staticmethod
    def cast_ability(ability, target, attacker):
        print(target.stats)
        hbefore = target.health
        damage = ability[1]['damage'][0] + attacker.stats['strength'] * ability[1]['damage'][1]
        damage = round(damage * (100 / (100 + target.stats['defense'])))
        target.health -= damage

        magic_damage = ability[1]['magic_damage'][0] + attacker.stats['intelligence'] * ability[1]['magic_damage'][1]
        magic_damage = round(magic_damage * (100 / (100 + target.stats['magic_defense'])))
        target.health -= magic_damage

        if len(ability[1]['effects']) > 0:
            for effect, duration in ability['effects']:
                target.effects.append((effect, duration))
                ef.start(effect, target)

        return bembed.abipart(ability, target, attacker, damage, magic_damage, hbefore)

    async def wait_for_player(self, cha):
        if self.end:
            return
        await cha.send(embed=bembed.player_turn(self.side1[0], self.side1, self.side2, self.message))
        turn = self.turn
        await asyncio.sleep(120)
        if turn == self.turn:
            await cha.send('timed out')
            self.remove_self()

    async def player_turn(self, par, msg, player):
        self.message.append('---**Ally Turn**---')
        if self.end:
            return
        playeringame = [ing for ing in self.side1 if player.id == ing.id][0]
        if self.turn % 2 != 1:
            cha = msg.channel
            await cha.send('It\'s not your turn')
            return

        if playeringame.health < 1:
            return

        if par[0] == 'info':
            pass

        if par[0] == 'use':
            embed = await playeringame.use_ability(self, 1, par, msg)
            if embed != None:
                self.message.append(bembed.abifinish(embed))
            else:
                return
            # await msg.channel.send(embed=bembed.show(self.side1, self.side2))
            self.turn += 1

            await self.check_win()
            await self.enemy_turn()

    async def enemy_turn(self):
        self.message.append('---**Enemy Turn**---')
        if self.end:
            return

        embeds = []
        for enemy in self.side2:
            if enemy.alive:
                text = await enemy.turn(self)
                embeds.append(text)
                asyncio.wait(1)

        self.message.append(bembed.abicomp(embeds))
        self.turn += 1
        await self.check_win()
        self.update()
        await self.wait_for_player(self.channel)

    async def check_win(self):
        embeds = []
        side1_dead = True
        for char in self.side1:
            side1_dead = side1_dead and (char.health < 1)
            if char.health < 1 and char.alive == True:
                embeds.append(bembed.dead(char))
                char.alive = False

        side2_dead = True
        for char in self.side2:
            side2_dead = side2_dead and (char.health < 1)
            if char.health < 1 and char.alive == True:
                embeds.append(bembed.dead(char))
                char.alive = False

        if len(embeds) > 0:
            self.message.append(bembed.deadcomp(embeds))
            # await self.channel.send(embed=bembed.abicomp(embeds))

        if side2_dead == True:
            self.end = True
            await self.win()
            return

        if side1_dead == True:
            self.end = True
            await self.lose()
            return

    def update(self):
        for char in self.side1:
            print(char.abilities)
            for abi in char.abilities:
                if abi[1] == 1:
                    abi[1] = 0
                if abi[1] > 0:
                    abi[1] -= int(abi[1]) - 1
            print(char.abilities)

    def update_effects(side):
        for char in side:
            for effect in char.effects:
                effect[1] = int(effect[1]) - 1
                if effect[1] < 1:
                    char.effects.remove(effect)
                    ef.end(effect[0], char)
                else:
                    ef.tick(effect[0], char)

    async def win(self):
        winners = [char for char in self.side1 if char.isplayer == True]
        for winner in winners:
            player = core.GET.player(winner.id)
            loot = await player.give_item_bulk(self.data['loot'])
        self.message.append(bembed.win(self, winners, loot))
        await self.channel.send(embed=bembed.link(self.message))
        self.remove_self()

    async def lose(self):
        self.message.append(bembed.lose(self))
        await self.channel.send(embed=bembed.link(self.message))
        self.remove_self()


class Player:

    def __init__(self, player):
        dict_to_obj(player.__dict__, self)
        abis = self.abilities.copy()
        self.abilities = []
        for abi in abis:
            item = [abi, abilitydata[abi]['cooldown']]
            self.abilities.append(item)

        self.effects = []
        print(self.user)
        self.name = self.user.mention
        self.health = 100 + self.level * 20
        self.isplayer = True
        self.alive = True
        print(self.__dict__)

    async def use_ability(self, battle, side, par, msg):
        if side == 1:
            allyside = [ally if ally.health > 0 else None for ally in battle.side1]
            enemyside = [enemy if enemy.health > 0 else None for enemy in battle.side2]
        else:
            allyside = [ally if ally.health > 0 else None for ally in battle.side2]
            enemyside = [enemy if enemy.health > 0 else None for enemy in battle.side1]

        try:
            par[1] = int(par[1]) - 1
            par[2] = int(par[2]) - 1
        except Exception:
            return

        ability = par[1]
        try:
            ability = abilitydata[self.abilities[par[1]][0]]
        except Exception:
            await msg.channel.send('not a valid ability')
            return

        if self.abilities[par[1]][1] > 0:
            await msg.channel.send('ability on cooldown')
            return

        target = ability['target'][0]

        if target == 'enemy':
            if len(enemyside) < 2:
                target = enemyside[0]
            else:
                try:
                    target = enemyside[par[2]]
                except Exception:
                    await msg.channel.send('not a valid target')
                    return
                if target == None:
                    await msg.channel.send('this character is already dead')
                    return
        elif target == 'ally':
            pass
        elif target == 'enemy_all':
            pass
        elif target == 'ally_all':
            pass
        elif target == 'all':
            pass
        else:
            raise Exception('Ability doesnt have good target')

        abilityname = self.abilities[par[1]][0]
        ability = (abilityname, ability)
        self.abilities[par[1]][1] = abilitydata[abilityname]['cooldown']
        return Battle.cast_ability(ability, target, self)


class Enemy:
    data = load_enemies()

    def __init__(self, enemytype, level):
        self.name = enemytype
        self.level = level
        self.enemytype = enemytype
        if enemytype in Enemy.data:
            dict_to_obj(Enemy.data[enemytype], self)
        else:
            raise Exception('Enemy type does not exist')
        self.health = self.health[0] + self.health[1] * level
        self.health = round(self.health)
        self.effects = []
        self.isplayer = False
        self.alive = True
        print('stats:' + str(self.stats))

        print(self.__dict__)

    async def turn(self, battle):
        target, ability = AI.choose_ability(battle, self)
        print((target, ability))
        ability = (ability, abilitydata[ability])
        print(ability)

        embed = Battle.cast_ability(ability, target, self)
        return embed
