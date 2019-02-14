from core import GET
from social import character_creation
from social import new_user
import social
from files import User
from lobby import new_battle
from battle import Battle
import formatting as form
import asyncio
import trading
import discord
import info


async def execute(par, msg):
    cha = msg.channel
    player = GET.player(msg.author.id)

    if player is not None:
        player.reload()

    if par[0] == 'info':
        await info.info(par, player, cha)

    if par[0] in ['self', 'me']:
        await info.info(['info', 'player', 'self'], player, cha)

    if par[0] == 'commands':
        list_of_commands = form.list_commands(player)
        await cha.send(embed=form.commands(list_of_commands))

    if par[0] == 'help':
        await cha.send(embed=form.help())
        return

    if par[0] == 'deletecharacter':
        await social.delete_account(par, msg, player)
        return

    if player == None:
        if par[0] == 'join':
            player = new_user(msg.author)
            await character_creation(par, msg, player)
        else:
            await cha.send(embed=form.join())
        return

    if par[0] == 'join':
        await cha.send('You already joined!')

    if par[0] == 'tutorial':
        pass  # stuff

    if par[0] in ['battle', 'b']:
        await new_battle(par, msg, player)

    if par[0] in ['e', 'equip']:
        print('hi')
        if par[1] in player.inventory:
            equipped = player.equip(par[1])
            if equipped is None:
                await cha.send('Item already equipped')
            else:
                await cha.send(equipped)
        else:
            await cha.send('Item not in your inventory')

    if par[0] in ['ue', 'unequip']:
        unequipped = player.unequip(par[1])
        if unequipped is None:
            await cha.send('Item not equipped')
        elif unequipped == 'No gear':
            await cha.send('You are not wearing any gear there.')
        else:
            await cha.send(unequipped)

    if par[0] in ['s', 'sell']:
        sold = await trading.sell_item(par, msg, player)

    if par[0] in ['r', 'roll']:
        rolled = await trading.roll(par, msg, player)
        await asyncio.sleep(2)
        await cha.send(rolled)


async def answer(par, msg):
    cha = msg.channel

    if GET.player(msg.author.id) is None:
        return
    player = GET.player(msg.author.id)
    if par[0] == 'info':
        await info.info(par, player, cha)
        return
    print('ans')
    player = GET.player(msg.author.id)
    if player.status[0] == 'creator':
        await character_creation(par, msg, player)
        return

    if par[0] == 'deletecharacter':
        await social.delete_account(par, msg, player)
        return

    if player.status[0] == 'battle':
        battle = GET.battle(player.status[1])
        if battle.channel == cha:
            await battle.player_turn(par, msg, player)

    if player.status[0] == 'in lobby':
        lobby = GET.lobby(player.status[1])
        if lobby.channel == cha:
            await lobby.on_message(par, msg, player)
