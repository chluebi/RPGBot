
from . import effects as ef
from formatting import Battleembed as bembed


def cast_ability(ability, target, attacker):
    print('{} used {} on {}'.format(attacker.name, ability[0], target.name))
    if len([effect for effect, duration in attacker.effects if effect in ef.cripef]) > 0:
        return '{0.name} missed their turn.'.format(attacker)

    hbefore = target.health
    damage = ability[1]['damage'][0] + attacker.stats['strength'] * ability[1]['damage'][1]
    if damage > 0:
        damage = round(damage * (100 / (100 + target.stats['defense'])))
    else:
        damage = round(damage)
    target.health -= damage

    magic_damage = ability[1]['magic_damage'][0] + attacker.stats['intelligence'] * ability[1]['magic_damage'][1]
    if magic_damage > 0:
        magic_damage = round(magic_damage * (100 / (100 + target.stats['magic_defense'])))
    else:
        magic_damage = round(magic_damage)
    target.health -= magic_damage

    if len(ability[1]['effects']) > 0:
        for effect, duration in ability[1]['effects']:
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
