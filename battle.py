import json
import core
import random
import asyncio
from files import dict_to_obj
from formatting import Battleembed as bembed


abilitypath = 'Data/Game/Abilities.json'
abilitydata = json.load(open(abilitypath))


async def new_battle(par, msg, player):
    if player.status[0] == 'battle':
        msg.channel.send('You already are in a battle!')
        return

    if par[1] == 'tutorial':
        await Battles.start_battle('tutorial', player, msg.channel)


class Battles:
    battlepath = 'Data/Game/Battles.json'
    data = json.load(open(battlepath))

    @staticmethod
    async def start_battle(name, player, cha):
        if name in Battles.data:
            battledata = Battles.data[name]
        else:
            raise Exception('Battle not found')
        battle = Battle(battledata, player, cha)
        core.battles.append(battle)
        await battle.wait_for_player(cha)


class Battle:

    def __init__(self, data, player, cha):
        rand = -1
        usedrands = [battle.id for battle in core.battles]
        while rand in usedrands or rand == -1:
            rand = random.randint(0, 1000)
        self.id = rand
        self.side1 = [Player(player)]
        self.channel = cha
        player.status = ['battle', self.id]
        print(player.__dict__)
        self.side2 = [Enemy(enemytype, level) for enemytype, level in data['enemies']]
        names = []
        amount = []
        for character in self.side2:
            if character.name not in names:
                names.append(character.name)
                amount.append(1)
                character.name = character.name + '1'
            else:
                index = names.index(character.name)
                character.name = character.name + str((amount[index] + 1))
                amount[index] = amount[index] + 1

        self.turn = 1
        print(self.__dict__)

    def remove_self(self):
        i = 0
        for battle in core.battles:
            if battle.id == self.id:
                core.battles.pop(i)
            i += 1

    def check_win(self):
        win = True
        for fighter in side1:
            win = fighter.health < 1 and win

        if win is True:
            return 2

        win = True
        for fighter in side2:
            win = fighter.health < 1 and win

        if win is True:
            return 1

    @staticmethod
    def cast_ability(ability, target, attacker):
        damage = ability['damage'][0] + attacker.stats['strength'] * ability['damage'][1]
        target.health -= damage * (100 / 100 + target.stats['defense'])

        magic_damage = ability['magic_damage'][0] + attacker.stats['intelligence'] * ability['magic_damage'][1]
        target.health -= magic_damage * (100 / 100 + target.stats['magic_defense'])

        for effect, duration in ability['effects']:
            target.effects.append((effect, duration))

        return Battleembed.ability(ability, target, attacker, damage, magic_damage)

    async def wait_for_player(self, cha):
        await cha.send(embed=bembed.player_turn(self.side1[0], self.side2))
        turn = self.turn
        await asyncio.sleep(30)
        if turn == self.turn:
            await cha.send('timed out')
            self.remove_self()

    async def player_turn(self, par, msg, player):
        playeringame = [ing for ing in side1 if player.id == ing.id][0]
        if self.turn % 2 != 1:
            cha = msg.channel
            await cha.send('It\'s not your turn')
            return

        if par[0] == 'info':
            pass

        if par[0] == 'use':
            await playeringame.use_ability(self, 1, par, msg)

    def enemy_turn():
        pass


class Player:

    def __init__(self, player):
        dict_to_obj(player.__dict__, self)
        abis = self.abilities.copy()
        self.abilities = []
        for abi in abis:
            item = (abi, abilitydata[abi]['cooldown'])
            self.abilities.append(item)

        self.effects = []
        self.name = self.user.mention
        print(self.__dict__)

    def use_ability(battle, side, par, msg):
        if side == 1:
            allyside = [ally for ally in battle.side1 if ally.health > 0]
            enemyside = [enemy for enemy in enemy.side2 if enemy.health > 0]
        else:
            allyside = [ally for ally in battle.side2 if ally.health > 0]
            enemyside = [enemy for enemy in enemy.side1 if enemy.health > 0]

        ability = par[1]
        try:
            ability = abilitydata[Player.abilities[par[1]][0]]
        except Exception:
            msg.channel.send('not a valid ability')

        if Player.abilities[par[1]][1] > 0:
            msg.channel.send('ability on cooldown')

        target = ability['target'][0]

        if target == 'enemy':
            if len(enemyside) < 2:
                target = enemyside[0]
            else:
                try:
                    target = enemyside[par[2]]
                except Exception:
                    msg.channel.send('not a valid target')
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

        Battle.cast_ability(ability, target, self)


class Enemy:
    enemypath = 'Data/Game/Enemies.json'
    data = json.load(open(enemypath))

    def __init__(self, enemytype, level):
        self.name = enemytype
        self.level = level
        self.enemytype = enemytype
        if enemytype in Enemy.data:
            dict_to_obj(Enemy.data[enemytype], self)
        else:
            raise Exception('Enemy type does not exist')
        self.health = self.health[0] + self.health[1] * level
        self.heatlh = round(self.health)
        self.effects = []

        print(self.__dict__)

    def turn(self, battle):
        pass
