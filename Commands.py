from core import GET
from social import character_creation
import formatting
import discord


async def execute(par, msg):
    cha = msg.channel

    if par[0] == 'info':
        await cha.send(embed=formatting.info())
        return

    if par[0] == 'help':
        pass  # some helpful commands
        return

    if GET.player(msg.author.id) == None:
        if par[0] == 'join':
            await character_creation(msg)
        else:
            await cha.send(embed=formatting.join())
        return

    if par[0] == 'commands':
        pass  # available commands


async def answer(par, msg):
    pass
