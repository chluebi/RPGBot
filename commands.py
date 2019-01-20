from core import GET
from social import character_creation
from social import new_user
from files import User
from battle import new_battle
from battle import Battle
import formatting
import discord


async def execute(par, msg):
    cha = msg.channel
    player = GET.player(msg.author.id)

    if par[0] == 'info':
        await cha.send(embed=formatting.info())
        return

    if par[0] == 'help':
        await cha.send(embed=formatting.help())
        return

    if player == None:
        if par[0] == 'join':
            player = new_user(msg.author)
            await character_creation(par, msg, player)
        else:
            await cha.send(embed=formatting.join())
        return

    if par[0] == 'join':
        await cha.send('You already joined!')

    if par[0] == 'commands':
        pass  # available commands

    if par[0] == 'tutorial':
        pass  # stuff

    if par[0] in ['battle', 'b']:
        await new_battle(par, msg, player)


async def answer(par, msg):
    cha = msg.channel
    if GET.player(msg.author.id) is None:
        return
    print('ans')
    player = GET.player(msg.author.id)
    if player.status[0] == 'creator':
        await character_creation(par, msg, player)
    if player.status[0] == 'battle':
        battle = GET.battle(player.status[1])
        if battle.channel == cha:
            await battle.player_turn(par, msg, player)
