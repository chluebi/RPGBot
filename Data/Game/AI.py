import random
from Data.Game import effects as ef


def choose_ability(battle, char):
    if char.side == 1:
        allyside = battle.side1.copy()
        enemyside = battle.side2.copy()
    elif char.side == 2:
        allyside = battle.side2.copy()
        enemyside = battle.side1.copy()
    else:
        raise Exception('char has no side')

    for character in enemyside:
        for effect in ef.nottargetef:
            if ef.has_effect(effect, char):
                enemyside.remove(character)

    index = char.index

    if char.enemytype == 'goblin':
        target = min(enemyside, key=lambda enemy: enemy.health)
        abi = char.abilities[0]
        return (target, char.abilities[0])

    abi = random.choice(char.abilities)
    abistuff = abidata[abi]
    target = abistuff['target'][0]
    print(abistuff)
    print(target)
    if target == 'enemy':
        return (random.choice(enemyside), abi)
    elif target == 'ally':
        return (random.choice(allyside), abi)
    elif target == 'enemy_all':
        return (enemyside, abi)
    elif target == 'ally_all':
        return (allyside, abi)
    elif target == 'self':
        return (char, abi)
    else:
        raise Exception('not a good target')
