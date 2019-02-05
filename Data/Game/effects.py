

import json
import os

# effects that make you miss your turn
cripef = ['freeze']
nottargetef = ['shadowed']


def load_effects():
    effectpath = 'Data/Game/Effects/'
    effectdata = {}
    for file in os.listdir(effectpath):
        name, ext = os.path.splitext(file)
        effectdata[name] = json.load(open(effectpath + file))
    return effectdata


effectdata = load_effects()


def load_emoji():
    emoji = {}
    for key, value in effectdata.items():
        emoji[key] = value['emoji']

    return emoji


def has_effect_list(eflist, target):
    end = False
    for ef in eflist:
        end = has_effect(ef, target) or end

    return end


def has_effect(ef, target):
    if ef in [effect for effect, duration in target.effects]:
        return True
    else:
        return False


def get_effect(ef, target):
    return [[effect, duration] for effect, duration in target.effects if effect == ef][0]


def remove_ef(ef, target):
    if has_effect(ef, target):
        to_remove = [[effect, duration] for effect, duration in target.effects if effect == ef][0]
        target.effects.remove(to_remove)
        end(to_remove, target)
        print('removed {}'.format(ef))
    else:
        print('couldnt remove {}'.format(ef))


def start(ef, target):
    if ef == 'burn':
        remove_ef('freeze', target)
    if ef == 'freeze':
        remove_ef('burn', target)
    if ef == 'shielded':
        target.stats['defense'] += 500
    if ef == 'magic_barrier':
        target.stats['magic_defense'] += 500
    if ef == 'strength':
        target.stats['strength'] += 50
    if ef == 'intelligence':
        target.stats['intelligence'] += 50
    if ef == 'invincible':
        target.stats['magic_defense'] += 100000
        target.stats['defense'] += 100000
    if ef == 'cursed':
        remove_ef('strength', target)
        remove_ef('intelligence', target)
        for stat, value in target.stats.items():
            value -= 20


def tick(ef, target):
    if ef == 'burn':
        target.health -= 5
        return 'Burn 🔥 hits {0.name} for 5 damage'.format(target)
    if ef == 'freeze':
        return '{0.name} ❄️ is frozen'.format(target)
    if ef == 'bleed':
        dmg = (target.maxhealth - target.health) / 100
        target.health -= dmg
        return '{0.name} 💉 is bleeding for {} damage'.format(target, dmg)
    if ef == 'shadowed':
        return '{0.name} 🌑 moves in the shadows'.format(target, dmg)
    if ef == 'shielded':
        return '{0.name} 🛡️ hides behind the shield'.format(target, dmg)
    if ef == 'magic_barrier':
        return '{0.name} 🔰️ is protected by a magic barrier'.format(target, dmg)
    if ef == 'strength':
        return '{0.name} 💪️ is full of strength'.format(target, dmg)
    if ef == 'intelligence':
        return '{0.name} 🧠️ is clear minded'.format(target, dmg)
    if ef == 'cleanse':
        for ef in target.effects:
            remove_ef(ef[0], target)
        return '{0.name} 😶️ is immune to effects'.format(target, dmg)
    if ef == 'invincible':
        return '{0.name} 🔱️ is busy not taking damage'.format(target, dmg)
    if ef == 'cursed':
        return '{0.name} 🎃️ suffers under a curse'.format(target, dmg)
    return None


def end(ef, target):
    if ef == 'burn':
        return '{0.name} has stopped burning'.format(target)

    if ef == 'freeze':
        return '{0.name} is no longer frozen'.format(target)

    if ef == 'bleed':
        return '{0.name} has stopped bleeding'.format(target)

    if ef == 'shadowed':
        return '{0.name} has emerged from the shadows'.format(target)

    if ef == 'shielded':
        target.stats['defense'] -= 500
        return '{0.name} is no longer protected by the shield'.format(target)

    if ef == 'magic_barrier':
        target.stats['magic_defense'] -= 500
        return '{0.name} is no longer protected by the magic barrier'.format(target)

    if ef == 'strength':
        target.stats['strength'] -= 50
        return '{0.name} has lost their extra strength'.format(target)

    if ef == 'intelligence':
        target.stats['intelligence'] -= 50
        return '{0.name} has lost their extra intelligence'.format(target)

    if ef == 'cleanse':
        return '{0.name} is no longer immune against effects'.format(target)

    if ef == 'invincible':
        return '{0.name} can take damage again'.format(target)

    if ef == 'cursed':
        for stat, value in target.stats.items():
            value += 20
        return '{0.name} can take damage again'.format(target)
