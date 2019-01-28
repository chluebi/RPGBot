
from formatting import Battleembed as bembed
import formatting as form

# effects that make you miss your turn
cripef = ['freeze']


emoji = {}
emoji['freeze'] = '❄️'
emoji['burn'] = '🔥'

form.emoji = emoji
print(form.emoji)


def remove_ef(ef, target):
    if ef in [effect for effect, duration in target.effects]:
        to_remove = [[effect, duration] for effect, duration in target.effects if effect == ef][0]
        target.effects.remove_ef(to_remove)
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
        return 'Burn hits {0.name} for 5 damage'.format(target)
    if ef == 'freeze':
        return '{0.name} is frozen'.format(target)
    return None


def end(ef, target):
    pass
