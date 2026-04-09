import importlib
import random

class Player:
    def __init__(self):
        self.alive = True
        self.room = None
        self.items = []
        self.game = None

    def setGame(self, game):
        self.game = game

    def isAlive(self):
        return self.alive

    def kill(self):
        self.alive = False
        print('Oh no. You appear to be dead!')
        anotherGo = input('Want another go? (y/n) ').upper()
        if anotherGo == 'Y':
            print('You magically un-ghost. I wonder where your body will end up?')
            self.setRoom(12)
            self.resuscitate()
        else:
            self.game.flipPlayStatus()

    def resuscitate(self):
        self.alive = True

    def setRoom(self, room):
        self.room = room

    def getRoom(self):
        return self.room

    def look(self):
        room = self.game.getRoom(self.getRoom())
        print(room.getLongDesc())
        for thing in room.getContains():
            print('A', thing.getShortDesc(), 'is here.')
        if self.game.settings.get('show_exits', True) or self.game.settings.get('debug', False):
            exits = room.getExits()
            keys = ', '.join(exits.keys()) if exits else 'None!'
            print('Exits:', keys)

    def lookItem(self, noun):
        found = False
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing is not None:
            print(thing.getLongDesc())
            found = True
        thing = self.hasItem(noun)
        if thing is not None:
            print(thing.getLongDesc())
            found = True
        if not found:
            print('I cannot find one of them!')

    def hasItem(self, lookingFor):
        for item in self.items:
            if item.getShortDesc().upper() == lookingFor.upper():
                return item
        return None

    def getItem(self, noun):
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing is not None:
            self.items.append(thing)
            room.remove(thing)
            print('You manage to get a', noun.lower())
            if not thing.isGettable():
                print('Uh-oh... you struggle to hold a', noun.lower())
                self.dropItem(noun)
        else:
            print('You cannot find a', noun.lower())

    def dropItem(self, noun):
        room = self.game.getRoom(self.getRoom())
        thing = self.hasItem(noun)
        if thing is not None:
            room.putIn(thing)
            self.items.remove(thing)
            print('You drop a', noun.lower())
        else:
            print('You do not have a', noun.lower(), 'to drop!')

    def move(self, direction):
        """Move in a direction. Returns True if successful."""
        room = self.game.getRoom(self.getRoom())
        exits = room.getExits()
        if exits and direction in exits.keys():
            print('\nYou move.\n')
            self.room = exits[direction]
            self.look()
            return True
        else:
            print('I cannot move that way')
            return False

    def listItems(self):
        count = 0
        print('Things you are holding:')
        for item in self.items:
            print('-', item.getShortDesc())
            count += 1
        if count == 0:
            print('- Nothing!')

    def doCommand(self, verb, noun):
        try:
            module = importlib.import_module(f'commands.{verb.lower()}')
            module.execute(self, noun)
        except ModuleNotFoundError:
            print('Unknown command. Type HELP for help.')
        except Exception as e:
            print(f'Something went wrong: {e}')

    def getCommand(self):
        prompt = self.game.settings.get('input_prompt', 'What do you want to do? ')
        command = input(prompt).upper()
        commands = command.split(' ')
        while True:
            if len(commands) == 1:
                self.doCommand(commands[0], None)
                break
            elif len(commands) == 2:
                self.doCommand(commands[0], commands[1])
                break
            else:
                print('Please enter a verb followed by an optional noun.')
                print('Type HELP for help.')
