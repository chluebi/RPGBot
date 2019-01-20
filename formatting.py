from discord import Embed
from core import Tokens

prefix = Tokens.prefix()


def join():
    embed = Embed(title='Join', description='To use this bot, you first have to create a character', color=0x009fff)
    embed.add_field(name='>join', value='to create your character')
    return embed


def info():
    embed = Embed(title='Info', url=invite(), description='This is a RPG Bot', color=0x00fff3)
    embed.add_field(name='Help', value='>help', inline=True)
    embed.add_field(name='Commands', value='>commands', inline=True)
    embed.set_footer(text='Wanna add me to your server?')
    return embed


def help():
    embed = Embed(title='Help', url=invite(), description='This is a RPG Bot', color=0x00fff3)
    embed.add_field(name='>join', value='Join the Game', inline=False)
    embed.add_field(name='>info', value='Shows basic info about the bot', inline=True)
    embed.add_field(name='>commands', value='Shows a list of helpful commands', inline=True)
    embed.set_footer(text='Wanna add me to your server?')
    return embed


def invite():
    return 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=201848896'.format(Tokens.client())


def enum_choices(tuplearray):
    embed = Embed(title='Options', description='Choose an option', color=0x00fff3)
    i = 1
    for name, key in tuplearray:
        name = '``{}{}``   {}'.format(prefix + prefix, i, name)
        value = key
        embed.add_field(name=name, value=value, inline=False)
        i += 1
    return embed


def numerate(array):
    finished = []
    i = 1
    for name in array:
        finished.append('``{}``   {}'.format(i, name))
        i += 1

    finished = '\n'.join(finished)

    return finished


def alphabet(array):
    abc = 'abcdefghijklmnopqrstuvwxyz'
    finished = []
    i = 0
    for name in array:
        finished.append('``{}``   {}'.format(abc[i], name))
        i += 1

    finished = '\n'.join(finished)

    return finished


class Battleembed:

    def player_turn(player, allyside, enemyside):

        abilities = player.abilities
        embed = Embed(title='Battle', description='{}info <thing> to get more info'.format(prefix + prefix), color=0x00fff3)
        allies = allyside
        allies = ['{}({}hp)'.format(ally.name, ally.health) if ally.health > 0 else '~~{}~~'.format(ally.name) for ally in allies]
        embed.add_field(name='{}use'.format(prefix + prefix), value=alphabet(allies), inline=True)
        abilities = ['{}'.format(ability[0]) if ability[1] < 1 else '~~{}({}cd)~~'.format(ability[0], ability[1]) for ability in abilities]
        embed.add_field(name='<ability>', value=numerate(abilities), inline=True)

        enemies = enemyside
        enemies = ['{}({}hp)'.format(enemy.name, enemy.health) if enemy.health > 0 else '~~{}~~'.format(enemy.name) for enemy in enemies]
        embed.add_field(name='<target>', value=numerate(enemies), inline=True)

        return embed

    def ability(ability, target, attacker, damage, mdamage, hbefore):
        print(damage)
        print(mdamage)
        print(target.health)
        embed = Embed(title='Battle Event', description='{} used {} on {}'.format(attacker.name, ability[0], target.name), color=0x00fff3)
        before = hbefore
        string = '{} - **{}** - *{}* = {}'.format(before, damage, mdamage, target.health)
        embed.add_field(name='Damage', value=string, inline=True)
        if len(ability[1]['effects']) > 0:
            embed.add_field(name='Effects', value=['{} - {} turns'.format(effect, length) for effect, length in ability[1]['effects']], inline=True)

        return embed

    def show():
        pass
