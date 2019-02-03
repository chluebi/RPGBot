from files import load_gear
from random import randint, choice
import asyncio


def define_selltable():
    selltable = {}
    selltable['very common'] = 20
    selltable['common'] = 50
    selltable['rare'] = 100
    selltable['very rare'] = 100
    selltable['epic'] = 400
    selltable['legendary'] = 1000
    return selltable


def define_raritytable():
    raritytable = {}
    raritytable['very common'] = 100
    raritytable['common'] = 50
    raritytable['rare'] = 20
    raritytable['very rare'] = 10
    raritytable['epic'] = 5
    raritytable['legendary'] = 1
    return raritytable


selltable = define_selltable()
raritytable = define_raritytable()
gear = load_gear()


async def sell_item(par, msg, player):
    cha = msg.channel

    try:
        name = par[1]
        amount = player.inventory[par[1]]
    except:
        await cha.send('Item not found.')
        return

    try:
        sellamount = int(par[2])
    except:
        sellamount = 1

    if amount < sellamount + 1:
        if player.equipped[gear[par[1]]['position']] == name:
            unequipped = player.unequip(gear[par[1]]['position'])
            await cha.send(unequipped)
    try:
        rarity = gear[par[1]]['rarity']
        temp = selltable[rarity]
    except:
        await cha.send('Not a sellable Item.')
        return

    await player.give_item('gold', selltable[rarity] * sellamount)
    await player.give_item(par[1], -sellamount)
    player.save_self()

    await cha.send('Sold {} of {}'.format(sellamount, par[1]))


async def roll(par, msg, player):
    gear = load_gear()
    rollables = {}
    for key, value in gear.items():
        if value['rarity'] != '0':
            rollables[key] = value

    raritytable = define_raritytable()

    rarity = 'common'
    RNG = randint(0, 100)

    for key, value in raritytable.items():
        if value > RNG:
            rarity = key

    all_with_rarity = []
    for key, value in gear.items():
        if value['rarity'] == rarity:
            all_with_rarity.append(key)

    drop = choice(all_with_rarity)

    if player.inventory['gold'] < 100:
        return 'Not enough gold'

    await player.give_item('gold', -100)
    await player.give_item(drop, 1)
    return 'Rolled **{}** for 100 gold'.format(drop)
