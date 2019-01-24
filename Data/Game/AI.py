import random


def choose_ability(battle, char):
    if char.side == 1:
        allyside = battle.side1
        enemyside = battle.side2
    elif char.side == 2:
        allyside = battle.side2
        enemyside = battle.side1
    else:
        raise Exception('char has no side')

    index = char.index

    if char.enemytype == 'goblin':
        target = min(enemyside, key=lambda enemy: enemy.health)
        abi = char.abilities[0]
        return (target, char.abilities[0])

    return (random.choice(enemyside), random.choice(char.abilities))
