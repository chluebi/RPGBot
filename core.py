import json

users = []
battles = []


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
    def battle(identifier):
        for battle in battles:
            if battle.id == identifier:
                return battle

        return None
