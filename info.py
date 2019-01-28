from core import Tokens
import formatting as form
import json
from battle import load_abilities, load_battles, load_enemies
from battle import Battles


def all_battles(player):
    data = load_battles()[0]
    battlelist = ''
    for folder, content in data.items():
        battlelist += '**{}**\n'.format(folder)
        for key, value in content.items():
            if value['min_level'] <= player.level and value['min_level'] + 3 > player.level:
                battlelist += '- {} \n'.format(key)
        battlelist += '\n\n'

    return battlelist


def all_abilities(player):
    data = load_abilities()
    abilitylist = ''
    for key, value in data.items():
        if key in player.abilities:
            abilitylist += '**{}** \n'.format(key)
        else:
            abilitylist += '{} \n'.format(key)

    return abilitylist


def abilitiy_info(ability):
    data = load_abilities()

    if ability not in data:
        return form.basic('Not found', 'ability not found')

    endstring = ''
    abilitydata = data[ability]
    endstring += abilitydata['description'] + '\n\n'
    endstring += 'Targets '
    endstring += str(abilitydata['target'][1])
    if abilitydata['target'][1] == 1:
        if abilitydata['target'][0] == 'enemy':
            endstring += ' enemy'
    else:
        if abilitydata['target'][0] == 'enemy':
            endstring += ' enemies'

    endstring += '.\n'
    dmg = abilitydata['damage']
    if abilitydata['damage'][0] > 0 or abilitydata['damage'][1] > 0:
        endstring += 'Deals **{} (+ {}%  of strength)** damage \n'.format(dmg[0], dmg[1] * 100)
    if abilitydata['damage'][0] < 0 or abilitydata['damage'][1] < 0:
        endstring += 'Heals for **{} (+ {}%  of strength)** damage \n'.format(dmg[0], dmg[1] * 100)
    mdmg = abilitydata['magic_damage']
    if mdmg[0] > 0 or mdmg[1] > 0:
        endstring += 'Deals **{} (+ {}%  of intelligence)** magic damage \n'.format(mdmg[0], mdmg[1] * 100)
    if mdmg[0] < 0 or mdmg[1] < 0:
        endstring += 'Heals for **{} (+ {}%  of intelligence)** damage \n'.format(mdmg[0], mdmg[1] * 100)

    ef = abilitydata['effects']
    if len(ef) > 1:
        endstring += '\n'
        endstring += 'Gives the target(s) the following effects: '
        for effect, duration in ef[:-2]:
            effect = '**{}**'.format(effect)
            endstring += '**{}** ( {} turns), '.format(effect, duration)
        endstring += '**{0}** ( {1} turns) '.format(ef[-2][0], str(ef[-2][1]))
        endstring += 'and **{0}** ( {1} turns) '.format(ef[-1][0], str(ef[-1][1]))
    elif len(ef) == 1:
        endstring += '\n'
        endstring += 'Gives the target(s) the following effect: '
        endstring += '**{0}** ( {1} turns)'.format(ef[0][0], str(ef[0][1]))

    return form.basic('Ability info', endstring)


prefix = Tokens.prefix()


async def info(par, player, cha):
    if len(par) < 2:
        await cha.send(embed=form.info())
        return

    if par[1] in ['battle', 'battles']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Battles', all_battles(player)))
        else:
            embed = Battles.battle_info(par[2])
            await cha.send(embed=embed)

    if par[1] in ['abilities', 'ability']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Abilities', all_abilities(player)))
        else:
            embed = abilitiy_info(par[2])
            await cha.send(embed=embed)


async def commands(par, player, cha):
    commands = []
    status = player.status
    if status[0] == 'None':
        commands.append(('{}battle <battle>'.format(prefix), 'Start a battle'))
        await cha.send(embed=form.commands(commands))

    if status[0] == 'battle':
        pass
