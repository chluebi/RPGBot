from core import Tokens, GET
import formatting as form
import json
from battle import load_abilities, load_battles, load_enemies
from files import load_gear
from Data.Game.effects import load_effects
from battle import Battles
from discord import Embed


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
    print(data)

    if ability not in data:
        return form.basic('Not found', 'ability not found')

    endstring = ''
    abilitydata = data[ability]
    endstring += abilitydata['description'] + '\n\n'
    endstring += 'Targets '
    if abilitydata['target'][0] == 'enemy_all':
        endstring += ' all enemies'
    elif abilitydata['target'][0] == 'ally_all':
        endstring += ' all allies'
    else:
        endstring += str(abilitydata['target'][1])
        if abilitydata['target'][1] == 1:
            if abilitydata['target'][0] == 'enemy':
                endstring += ' enemy'
            if abilitydata['target'][0] == 'ally':
                endstring += ' ally'
        else:
            if abilitydata['target'][0] == 'enemy':
                endstring += ' enemies'
            if abilitydata['target'][0] == 'ally':
                endstring += ' allies'

    endstring += '.\n'
    dmg = abilitydata['damage']
    if abilitydata['damage'][0] > 0 or abilitydata['damage'][1] > 0:
        endstring += 'Deals **{} (+ {}%  of strength) (+ {}%  of precision)** damage \n'.format(dmg[0], dmg[1] * 100, dmg[2] * 100)
    if abilitydata['damage'][0] < 0 or abilitydata['damage'][1] < 0:
        endstring += 'Heals for **{} (+ {}%  of strength) (+ {}%  of precision)** damage \n'.format(dmg[0], dmg[1] * 100, dmg[2] * 100)
    mdmg = abilitydata['magic_damage']
    if mdmg[0] > 0 or mdmg[1] > 0:
        endstring += 'Deals **{} (+ {}%  of intelligence) (+ {}%  of precision)** magic damage \n'.format(mdmg[0], mdmg[1] * 100, dmg[2] * 100)
    if mdmg[0] < 0 or mdmg[1] < 0:
        endstring += 'Heals for **{} (+ {}%  of intelligence) (+ {}%  of precision)** damage \n'.format(mdmg[0], mdmg[1] * 100, dmg[2] * 100)

    if 'random_multiplier' in abilitydata:
        ra = abilitydata['random_multiplier']
        endstring += 'Random Multiplier of **{}%** to **{}%** \n'.format(ra[0] * 100, ra[1] * 100)

    if 'crit_chance' in abilitydata:
        cr = abilitydata['crit_chance']
        endstring += 'Chance of **{}%** to mulitiply damage by **{}**% \n'.format(cr[0] * 100, cr[1] * 100)

    ef = abilitydata['effects']
    if len(ef) > 1:
        endstring += '\n'
        endstring += 'Gives the target(s) the following effects: '
        for full_effect in ef[:-2]:
            effect = full_effect[0]
            duration = full_effect[1]
            effect = '**{}**'.format(effect)
            endstring += '**{}** ( {} turns)'.format(effect, duration)
            if len(full_effect) > 2:
                endstring += ' ({}%  chance)'.format(full_effect[2] * 100)
            endstring += ', '
        if len(ef[-2]) > 2:
            endstring += '**{0}** ( {1} turns) ({2}%  chance)'.format(ef[-2][0], str(ef[-2][1]), str(ef[-2][2]) * 100)
        else:
            endstring += '**{0}** ( {1} turns) '.format(ef[-2][0], str(ef[-2][1]))
        if len(ef[-1]) > 2:
            endstring += 'and **{0}** ( {1} turns) ({2}%  chance)'.format(ef[-2][0], str(ef[-2][1]), str(ef[-2][2]) * 100)
        else:
            endstring += 'and **{0}** ( {1} turns) '.format(ef[-1][0], str(ef[-1][1]))
    elif len(ef) == 1:
        endstring += '\n'
        endstring += 'Gives the target(s) the following effect: '
        endstring += '**{0}** ( {1} turns)'.format(ef[0][0], str(ef[0][1]))

    print(endstring)
    return form.basic('Ability info', endstring)


def all_enemies():
    data = load_enemies()
    enemylist = ''
    for key, value in data.items():
        enemylist += '**{}** \n'.format(key)

    return enemylist


def all_items():
    data = load_gear()
    groups = {}
    for key, value in data.items():
        groups[value['position']] = []

    for key, value in data.items():
        groups[value['position']].append((key, value))

    for group_name, group in groups.items():
        print(group)

    itemlist = ''
    for group_name, group in groups.items():
        itemlist += '\n **{}** \n'.format(group_name)
        for key, value in group:
            itemlist += '{} \n'.format(key)

    return itemlist


def all_effects():
    data = load_effects()
    effectlist = ''
    for key, value in data.items():
        effectlist += '**{}** {} \n'.format(key, value['emoji'])

    return effectlist


def enemy_info(enemy):
    data = load_enemies()

    if enemy not in data:
        return None

    enemydata = data[enemy]
    endstring = ''

    endstring += enemydata['description'] + '\n\n'
    endstring += 'Health: '
    endstring += '{0[0]} (+ {0[1]} per level) \n\n'.format(enemydata['health'])
    for key, value in enemydata['stats'].items():
        endstring += '{0}: {1[0]} (+ {1[1]} per level) \n'.format(key, value)

    endstring += '\n Abilities: \n'
    for ability in enemydata['abilities']:
        endstring += '{} \n'.format(ability)

    return form.basic(enemy, endstring)


def ingame_enemy_info(enemy):
    data = load_enemies()
    enemydata = data[enemy.enemytype]
    endstring = ''

    endstring += 'Level: {} \n'.format(enemy.level)

    endstring += 'Health: '
    maxhealth = int(enemydata['health'][0]) + int(enemydata['health'][1]) * int(enemy.level)
    endstring += '{}/{} \n \n'.format(enemy.health, maxhealth)

    for stat, value in enemy.stats.items():
        datastat = enemydata['stats'][stat]
        datastat = int(datastat[0]) + int(datastat[1]) * int(enemy.level)
        if datastat != value:
            pass
        else:
            endstring += '{}: {} \n'.format(stat, value)

    if len(enemy.effects) > 0:
        endstring += '\n Effects: \n'
        for ef, dur in enemy.effects:
            endstring += '{} ({} turns left)'.format(ef, dur)

    return form.basic(enemy.name, endstring)


def user_info(searched_player, player):
    searched_player.reload()
    searched_clientuser = GET.clientuser(searched_player.id)
    endstring = ''
    endstring += '**ID:** {} \n'.format(searched_player.id)
    endstring += '**Status:** {} \n'.format(str(searched_player.status))
    endstring += '**Level:** {} \n'.format(searched_player.level)
    xplimit = ((searched_player.level + 1) * 100)
    endstring += '**XP:** {}/{} \n\n'.format(searched_player.xp, xplimit)
    endstring += '**Health: {}** \n'.format(searched_player.health)
    endstring += '**Stats:** \n'
    for key, value in searched_player.stats.items():
        endstring += '{}: {} \n'.format(key, value)
    endstring += '\n'
    endstring += '**Gear:** \n'
    for key, value in searched_player.equipped.items():
        endstring += '{}: {} \n'.format(key, value)
    endstring += '\n'
    endstring += '**Inventory:** \n'
    equipped = [value for key, value in searched_player.equipped.items()]
    for key, value in searched_player.inventory.items():
        if key in equipped:
            endstring += '*{}: {}* \n'.format(key, value)
        else:
            endstring += '{}: {} \n'.format(key, value)
    endstring += '\n'
    endstring += '**Abilities:** \n'
    for key in searched_player.abilities:
        endstring += '{} \n'.format(key)
    endstring += '\n'
    embed = Embed(title=searched_player.name, description=endstring, color=0x00ffa7)
    embed.set_author(name='searched by {0.name}'.format(player), icon_url=GET.clientuser(player.id).avatar_url)
    embed.set_thumbnail(url=searched_clientuser.avatar_url)
    return embed


def item_info(item):
    item2 = item
    item = load_gear()[item]
    endstring = ''
    endstring += item['description'] + '\n\n'
    endstring += 'Rarity: **{}** \n'.format(item['rarity'])
    endstring += 'Position: **{}** \n\n'.format(item['position'])
    for stat, value in item['stats'].items():
        endstring += '{}: **{}** \n'.format(stat, value)

    if len(item['abilities']) > 0:
        endstring += '\n Grants Abilities: \n'
        for ability in item['abilities']:
            endstring += '**{}** \n'.format(ability)

    return form.basic(item2, endstring)


def effect_info(effect):
    effect2 = effect
    effect = load_effects()[effect]
    effectname = '{} {}'.format(effect2, effect['emoji'])
    endstring = effect['description']

    return form.basic(effectname, endstring)


prefix = Tokens.prefix()


async def info(par, player, cha):
    if len(par) < 2:
        await cha.send(embed=form.info())
        return

    if par[1] in ['b', 'battle', 'battles']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Battles', all_battles(player)))
            return
        else:
            embed = Battles.battle_info(par[2])
            await cha.send(embed=embed)
            return

    if par[1] in ['a', 'abilities', 'ability']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Abilities', all_abilities(player)))
            return
        else:
            embed = abilitiy_info(par[2])
            await cha.send(embed=embed)
            return

    if par[1] in ['e', 'enemy']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Enemies', all_enemies()))
            return
        else:
            embed = enemy_info(par[2])
            if embed != None:
                await cha.send(embed=embed)
                return

            embed = None
            if player.status[0] == 'battle':
                battle = GET.battle(player.status[1])
                if par[2] in [en.name for en in battle.side1 + battle.side2]:
                    enemy = [en for en in battle.side1 + battle.side2 if en.name == par[2]][0]
                    embed = ingame_enemy_info(enemy)
                else:
                    embed = form.basic('Not found', 'enemy not found (enemy not found in battle)')
                    return
            else:
                embed = form.basic('Not found', 'enemy not found (not in battle)')
                return

            if embed != None:
                await cha.send(embed=embed)
                return
            else:
                await cha.send(embed=form.basic('Not found', 'enemy not found'))
                return

    if par[1] in ['user', 'player', 'u']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Not enough arguments', 'specify a User'))
            return
        if par[2] == 'self':
            searched_player = player
        else:
            searched_player = GET.player_by_name(par[2])
            searched_player = GET.player(searched_player)

        if searched_player is None:
            await cha.send(embed=form.basic('Not found', 'Player not found'))
            return
        else:
            await cha.send(embed=user_info(searched_player, player))
            return

    if par[1] in ['item', 'gear', 'i']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Items', all_items()))
            return

        items = load_gear()
        if par[2] not in items:
            await cha.send(embed=form.basic('Not found', 'Item not found'))
            return

        await cha.send(embed=item_info(par[2]))
        return

    if par[1] in ['ef', 'effect']:
        if len(par) < 3:
            await cha.send(embed=form.basic('Effects', all_effects()))
            return

        effects = load_effects()
        if par[2] not in effects:
            await cha.send(embed=form.basic('Not found', 'Effect not found'))
            return

        await cha.send(embed=effect_info(par[2]))
        return

    if len(par) == 2:
        all_data = {}
        all_data['ef'] = load_effects()
        all_data['e'] = load_enemies()
        all_data['i'] = load_gear()
        all_data['a'] = load_abilities()
        all_data['b'] = load_battles()[1]

        all_data2 = all_data.copy()
        singular_data = {}

        for category, value in all_data2.items():
            for key, value2 in value.items():
                singular_data[key] = value2
                singular_data[key]['category'] = category

        results = []

        for key, value in singular_data.items():
            if par[1] == key:
                if len(results) < 1:
                    results.append((key, value))
                else:
                    results[0] = (key, value)
            if par[1] in key:
                results.append((key, value))

        print(results)

        if len(results) < 1:
            return

        cat = results[0][1]
        print(cat)
        cat = cat['category']
        key = results[0][0]

        par = ['info', cat, key]

        print(par)

        await info(par, player, cha)


async def commands(par, player, cha):
    commands = []
    status = player.status
    if status[0] == 'None':
        commands.append(('{}battle <battle>'.format(prefix), 'Start a battle'))
        await cha.send(embed=form.commands(commands))

    if status[0] == 'battle':
        pass
