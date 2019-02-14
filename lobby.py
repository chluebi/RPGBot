import json
import core
import random
import asyncio
import discord
from formatting import Battleembed as bembed


client = discord.Client()


async def new_battle(par, msg, player):
    cha = msg.channel

    if player.status[0] == 'battle':
        await msg.channel.send('You already are in a battle!')
        return

    if len(player.abilities) < 1:
        await msg.channel.send('Equip some items first!')
        return

    if len(par) < 2:
        await msg.channel.send('Specify a battletype! More info with {}info battle'.format(prefix))
        return

    if par[1] == 'solo':
        if par[1] == 'tutorial':
            await Battles.start_battle('tutorial', player, msg.channel)
            return

        if par[1] in ['c', 'cave', 'cavelands']:
            await Battles.start_battle('Cavelands', player, msg.channel)
            return

        await Battles.start_battle(par[2], player, msg.channel)
        return

    if par[1] == 'pvp':
        if len(par) > 2:
            if par[2] in ['team']:
                message = await cha.send(embed=bembed.teambattle([], []))
                lobby = LobbyTeams(player, message)
                await lobby.message.add_reaction('1⃣')
                await lobby.message.add_reaction('2⃣')

                while lobby.cd > 0:
                    lobby.cd -= 1
                    await asyncio.sleep(1)

                    if lobby.cd % 2 == 0:
                        await lobby.update()

                    if lobby.status != 'waiting':
                        break

                if lobby.status == 'waiting':
                    await lobby.message.edit(embed=bembed.timeout())
                    lobby.remove_self()

            else:
                opponent_id = core.GET.player_by_name(par[2])
                if opponent_id is None:
                    await cha.send('Player not found')

                print(opponent_id)

                opponent = core.GET.player(opponent_id)
                if opponent is None:
                    await cha.send('Player not found')

                def check(reaction, user):
                    check1 = core.GET.player_by_name(str(user.id))
                    check1 = check1 is not None
                    check2 = str(reaction.emoji) == '✅'
                    clientplayer = core.GET.player(player.id)
                    print(user.id)
                    print(player.id)
                    check3 = user.id != player.id
                    check4 = user.bot is not True
                    check5 = user.id == opponent_id
                    return check1 and check2 and check3 and check4 and check5

                pvpmsg = await cha.send(embed=bembed.pvp_specific(player, opponent))
                await pvpmsg.add_reaction('✅')
                try:
                    user = await client.wait_for('reaction_add', check=check, timeout=180.0)
                    reaction, user = user
                except asyncio.TimeoutError:
                    await pvpmsg.edit(embed=bembed.timeout())
                    return

                opponent_id = core.GET.player_by_name(str(user.id))
                opponent = core.GET.player(opponent_id)

                await Battles.start_pvp([player], [opponent], cha)

                if opponent_id is None:
                    await msg.channel.send('Player not found!')

        else:
            def check(reaction, user):
                check1 = core.GET.player_by_name(str(user.id))
                check1 = check1 is not None
                check2 = str(reaction.emoji) == '✅'
                clientplayer = core.GET.player(player.id)
                print(user.id)
                print(player.id)
                check3 = user.id != player.id
                check4 = user.bot is not True
                return check1 and check2 and check3 and check4

            pvpmsg = await cha.send(embed=bembed.pvp(player))
            await pvpmsg.add_reaction('✅')
            try:
                user = await client.wait_for('reaction_add', check=check, timeout=180.0)
                reaction, user = user
            except asyncio.TimeoutError:
                await pvpmsg.edit(embed=bembed.timeout())
                return

            opponent_id = core.GET.player_by_name(str(user.id))
            opponent = core.GET.player(opponent_id)

            await Battles.start_pvp([player], [opponent], cha, None)

    if par[1] == 'raid':
        message = await cha.send(embed=bembed.raid([player]))
        lobby = LobbyRaid(player, message)
        await lobby.message.add_reaction('✅')
        player.status = ['in lobby', lobby.id]

        while lobby.cd > 0:
            lobby.cd -= 1
            await asyncio.sleep(1)

            if lobby.cd % 2 == 0:
                await lobby.update()

            if lobby.status != 'waiting':
                break

        if lobby.status == 'waiting':
            await lobby.message.edit(embed=bembed.timeout())
            lobby.remove_self()


class LobbyRaid:
    def __init__(self, admin, message):
        self.admin = admin
        self.message = message
        self.channel = message.channel
        self.id = core.set_id(4, core.lobbys)
        self.players = [admin]
        self.type = 'raid'
        self.cd = 600
        self.status = 'waiting'
        print(self.id)
        core.lobbys.append(self)

    async def get_reaction_users(self, emoji):
        for reaction in self.message.reactions:
            print(reaction)
            if reaction.emoji == emoji:
                reactors = []
                async for reactor in reaction.users():
                    print(reactor)
                    player = core.GET.player(reactor.id)
                    if player is None:
                        continue
                    if player is self.admin:
                        continue
                    if player.status != 'None':
                        continue
                    reactors.append(player)
                return reactors

    async def update(self):
        self.message = await self.channel.get_message(self.message.id)
        reactors = [self.admin]
        added_reactors = await self.get_reaction_users('✅')
        print(added_reactors)
        if added_reactors is not None:
            reactors += added_reactors
        self.players = reactors
        await self.message.edit(embed=bembed.raid(self.players))

    async def on_message(self, par, msg, player):
        if player is self.admin:
            if par[0] == 'start':
                if len(par) > 1:
                    await self.start(par[1])
                else:
                    await self.start('random')

    async def start(self, mode):
        self.status = 'matchmaking'
        await Battles.start_raid(self.players, mode, self.channel, self)

    def remove_self(self):
        core.lobbys.remove(self)


class LobbyTeams(LobbyRaid):
    def __init__(self, admin, message):
        self.admin = admin
        self.message = message
        self.channel = message.channel
        self.id = core.set_id(4, core.lobbys)
        self.team1 = []
        self.team2 = []
        self.type = 'teams'
        self.cd = 600
        self.status = 'waiting'
        print(self.id)
        core.lobbys.append(self)

    async def get_reaction_users(self, emoji):
        for reaction in self.message.reactions:
            if reaction.emoji == emoji:
                reactors = []
                async for reactor in reaction.users():
                    player = core.GET.player(reactor.id)
                    if player is None:
                        continue
                    if player.status != 'None':
                        continue
                    reactors.append(player)
                return reactors

    async def update(self):
        self.message = await self.channel.get_message(self.message.id)
        team1 = await self.get_reaction_users('1⃣')
        team2 = await self.get_reaction_users('2⃣')
        for player in team1:
            if player in team1 and player in team2:
                team2.remove(player)
        if team1 is not None:
            self.team1 = team1
        if team2 is not None:
            self.team2 = team2
        await self.message.edit(embed=bembed.teambattle(self.team1, self.team2))

    async def on_message(self, par, msg, player):
        if player is self.admin:
            if par[0] == 'start':
                await self.start()

    async def start(self):
        self.status = 'matchmaking'
        await Battles.start_raid(self.team1, self.team2, self.channel, self)


class Battles:
    async def start_pvp(side1, side2, cha, lobby):
        print('pvp battle starting {}, {}'.format(side1, side2))

    async def start_raid(players, battle, cha, lobby):
        print('raid battle starting {}, {}'.format(players, battle))


async def on_reaction_add(reaction, user):
    pass


async def on_reaction_remove(reaction, user):
    pass
