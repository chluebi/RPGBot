
from formatting import Battleembed as bembed
import formatting as form

# effects that make you miss your turn
cripef = ['freeze']


emoji = {}
emoji['freeze'] = '❄️'
emoji['burn'] = '🔥'

form.emoji = emoji
print(form.emoji)


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
        print('removed {}'.format(ef))
    else:
        print('couldnt remove {}'.format(ef))


def start(ef, target):
    if ef == 'burn':
        remove_ef('freeze', target)
    if ef == 'freeze':
        remove_ef('burn', target)


def tick(ef, target):
    if ef == 'burn':
        target.health -= 5
        return 'Burn 🔥 hits {0.name} for 5 damage'.format(target)
    if ef == 'freeze':
        return '{0.name} ❄️ is frozen'.format(target)
    return None


def end(ef, target):
    if ef == 'burn':
        return '{0.name} has stopped burning'.format(target)

    if ef == 'freeze':
        return '{0.name} is no longer frozen'.format(target)
