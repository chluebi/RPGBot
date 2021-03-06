import discord
import asyncio
import core
from core import Parsing
from core import GET
from core import Tokens
from files import User
import commands

client = discord.Client()


if __name__ == '__main__':

    @client.event
    async def on_ready():
        print('bot ready')
        game = discord.Game('{}info'.format(Tokens.prefix()))
        await client.change_presence(status=discord.Status.online, activity=game)
        core.clientusers = client.users
        users = User.load_all()

    @client.event
    async def on_message(message):
        msg = message
        cha = message.channel
        par = Parsing.parse_msg(message)
        if par is not None:
            await commands.execute(par, msg)
        else:
            par = Parsing.parse_ans(message)
            if par is not None:
                await commands.answer(par, msg)

    client.run(Tokens.discord())
