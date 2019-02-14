import json
import random

clientusers = []
users = []
battles = []
lobbys = []


class Parsing:
    classes = open('Data/Game/Classes.json', 'r+')
    classes = json.load(classes)
    '''
    classes_desc = {}
    for key, value in classes.items():
        classes_desc[key] = value['description']

    print(classes_desc)
    '''
    print(classes)

    @staticmethod
    def parse_msg(message):
        prefix = Tokens.prefix()
        if message.content[:len(prefix)] != prefix:
            return None
        if len(message.content) <= len(prefix):
            return None
        if message.content[:len(prefix) * 2] == prefix + prefix:
            return None
        parsedmsg = message.content[len(prefix):].split()
        parsedmsg = [msg.lower() for msg in parsedmsg]
        print(parsedmsg)
        return parsedmsg

    @staticmethod
    def parse_ans(message):
        prefix = Tokens.prefix()
        prefix = prefix + prefix
        if message.content[:len(prefix)] != prefix:
            return None
        if len(message.content) <= len(prefix):
            return None
        parsedmsg = message.content[len(prefix):].split()
        parsedmsg = [msg.lower() for msg in parsedmsg]
        print(parsedmsg)
        return parsedmsg


class Tokens:
    tokenfile = open('tokens.json', 'r+')
    tokens = json.load(tokenfile)

    @staticmethod
    def discord():
        return Tokens.tokens['discord']['token']

    @staticmethod
    def prefix():
        return Tokens.tokens['prefix']

    @staticmethod
    def client():
        return Tokens.tokens['discord']['client']


class GET:
    @staticmethod
    def player(identifier):
        for user in users:
            if user.id == identifier:
                return user

        return None

    @staticmethod
    def player_by_name(name):
        for user in users:
            #print('------ next user ------')
            discorduser = GET.clientuser(user.id)
            # print(str(user.name)[:len(name)].lower())
            if str(user.name)[:len(name)].lower() == name:
                return user.id
            # print(str(discorduser)[:len(name)].lower())
            if str(discorduser)[:len(name)].lower() == name:
                return user.id
            # print(str(user.id)[:len(name)].lower())
            if str(user.id)[:len(name)].lower() == name:
                return user.id
            # print(str(discorduser.id)[:len(name)].lower())
            if str(discorduser.id)[:len(name)].lower() == name:
                return user.id
            # print(str(discorduser.display_name)[:len(name)].lower())
            if str(discorduser.display_name)[:len(name)].lower() == name:
                return user.id
            # print(str(discorduser.discriminator)[:len(name)].lower())
            if str(discorduser.discriminator)[:len(name)].lower() == name:
                return user.id
        return None

    @staticmethod
    def battle(identifier):
        for battle in battles:
            if battle.id == identifier:
                return battle

        return None

    @staticmethod
    def clientuser(identifier):
        for user in clientusers:
            if user.id == identifier:
                return user

        return None

    @staticmethod
    def lobby(identifier):
        for lobby in lobbys:
            if lobby.id == identifier:
                return lobby

        return None

    @staticmethod
    def lobby_by_message(msgid, chaid):
        for lobby in lobbys:
            if lobby.message.id == msgid and lobby.channel.id == chaid:
                return lobby

        return None


def set_id(length, array):
    usedrands = [item.id for item in array]
    rand = -1
    while rand in usedrands or rand == -1:
        rand = random.randint(0, 10 ** (length - 1))

    return rand
