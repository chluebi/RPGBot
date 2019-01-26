from core import Tokens
import formatting as form
from battle import Battles


def avai(player):
    return Battles.available_battles(player)


prefix = Tokens.prefix()


async def info(par, player, cha):
    if len(par) < 2:
        await cha.send(embed=form.info())
        return

    if par[1] == 'battle':
        if len(par) < 3:
            await cha.send(embed=form.basic('Available Battles', avai(player)))
        else:
            embed = Battles.battle_info(par[2])
            await cha.send(embed=embed)


async def commands(par, player, cha):
    commands = []
    status = player.status
    if status[0] == 'None':
        commands.append(('{}battle <battle>'.format(prefix), 'Start a battle'))
        await cha.send(embed=form.commands(commands))

    if status[0] == 'battle':
        pass
