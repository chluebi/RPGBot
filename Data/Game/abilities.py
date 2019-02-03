
from . import effects as ef
from formatting import Battleembed as bembed
from random import randint


def cast_ability(ability, target, attacker):
    if isinstance(target, (list,)):
        if len(target) > 1:
            return '\n'.join([cast_ability(ability, targ, attacker) for targ in target])
        else:
            target = target[0]
    print('{} used {} on {}'.format(attacker.name, ability[0], target.name))
    if len([effect for effect, duration in attacker.effects if effect in ef.cripef]) > 0:
        return '{0.name} missed their turn.'.format(attacker)

    hbefore = target.health
    damage = ability[1]['damage'][0] + attacker.stats['strength'] * ability[1]['damage'][1] + attacker.stats['precision'] * ability[1]['damage'][2]
    if damage > 0:
        damage = round(damage * (100 / (100 + target.stats['defense'])))
    else:
        damage = round(damage)

    magic_damage = ability[1]['magic_damage'][0] + attacker.stats['intelligence'] * ability[1]['magic_damage'][1] + attacker.stats['precision'] * ability[1]['magic_damage'][2]
    if magic_damage > 0:
        magic_damage = round(magic_damage * (100 / (100 + target.stats['magic_defense'])))
    else:
        magic_damage = round(magic_damage)

    total_damage = damage + magic_damage

    if 'random_multiplier' in ability[1]:
        total_damage = total_damage * randint(ability[1]['random_multiplier'][0] * 100, ability[1]['random_multiplier'][1] * 100) / 100

    if 'crit_chance' in ability[1]:
        if randint(1, 100) <= ability[1]['crit_chance'][0] * 100:
            total_damage = total_damage * ability[1]['crit_chance'][1]

    total_damage = round(total_damage)

    target.health -= total_damage

    if len(ability[1]['effects']) > 0:
        for full_effect in ability[1]['effects']:
            effect = full_effect[0]
            duration = full_effect[1]
            if len(full_effect) > 2:
                if randint(1, 100) > full_effect[2] * 100:
                    continue
            print('added {} {} for to {}'.format(effect, duration, target.name))
            if not ef.has_effect(effect, target):
                target.effects.append([effect, duration])
                ef.start(effect, target)
            else:
                to_longer = ef.get_effect(effect, target)
                effect_index = target.effects.index(to_longer)
                print('original dur: {} new dur: {}'.format(to_longer[1], duration))
                to_longer[1] = max(to_longer[1], int(duration))
                print('new dur {}'.format(to_longer[1]))
                target.effects[effect_index][1] = to_longer[1]
            print(target.effects)

    return bembed.abipart(ability, target, attacker, damage, magic_damage, hbefore)
