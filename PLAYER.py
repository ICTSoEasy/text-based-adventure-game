import importlib
import importlib.util
import random

class Player:
    def __init__(self):
        self.alive = True
        self.room = None
        self.items = []
        self.game = None

    def isLocationLit(self):
        room = self.game.getRoom(self.getRoom())
        if room.isLit():
            return True
        for item in self.items:
            if item.getMakingLight():
                return True
        for item in room.getContains():
            if item.getMakingLight():
                return True
        return False

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
        debug = self.game.settings.get('debug', False)
        if self.isLocationLit():
            print(room.getLongDesc())
            for thing in room.getContains():
                room_desc = thing.getRoomDesc()
                if room_desc:
                    print(room_desc)
                else:
                    print('A', thing.getShortDesc(), 'is here.')
            if self.game.settings.get('show_exits', True) or debug:
                exits = room.getExits()
                keys = ', '.join(exits.keys()) if exits else 'None!'
                print('Exits:', keys)
        else:
            print(self.game.settings.get('dark_message'))
            if debug:
                exits = room.getExits()
                keys = ', '.join(exits.keys()) if exits else 'None!'
                print('Exits:', keys)

    def lookItem(self, noun):
        found = False
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing is not None:
            desc = thing.getLongDesc()
            print(desc if desc else self.game.messages.get('no_item_detail', 'Sorry but I am not allowed to give more detail.'))
            found = True
        thing = self.hasItem(noun)
        if thing is not None:
            desc = thing.getLongDesc()
            print(desc if desc else self.game.messages.get('no_item_detail', 'Sorry but I am not allowed to give more detail.'))
            found = True
        if not found:
            print('I cannot find one of them!')

    def hasItem(self, lookingFor):
        for item in self.items:
            if item.matchesName(lookingFor):
                return item
        return None

    def getItem(self, noun):
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing is not None:
            self.items.append(thing)
            room.remove(thing)
            #print('You manage to get a', noun.lower())
            print('OK.')
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
            print('OK.')
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

    def _expand_noun(self, noun):
        """If noun has no exact match but numbered variants exist locally (e.g. ROD1, ROD2), return them.
        Prefers items in the current room over inventory, so GET finds room items and DROP finds inventory items."""
        import re
        if noun is None:
            return [noun]
        if self.game.findItem(noun):
            return [noun]
        current_room = self.game.getRoom(self.getRoom())
        room_variants = []
        inv_variants = []
        for item in current_room.getContains():
            for word in item.idWords:
                if re.match(f'^{re.escape(noun)}\\d+$', word) and word not in room_variants:
                    room_variants.append(word)
        for item in self.items:
            for word in item.idWords:
                if re.match(f'^{re.escape(noun)}\\d+$', word) and word not in inv_variants:
                    inv_variants.append(word)
        variants = sorted(room_variants) or sorted(inv_variants)
        return [variants[0]] if variants else [noun]

    def doCommand(self, verb, noun, _expanded=False):
        # Expand bare noun to numbered variants if needed (e.g. ROD -> ROD1, ROD2)
        if not _expanded:
            nouns = self._expand_noun(noun)
            if len(nouns) > 1 or (nouns and nouns[0] != noun):
                for n in nouns:
                    self.doCommand(verb, n, _expanded=True)
                return

        # Remap Python keywords that can't be module names
        v = {'in': 'enter', 'return': 'back'}.get(verb.lower(), verb.lower())
        candidates = [
            f'commands.{v}',
            f'commands.game.{v}',
            f'commands.aliases.{v}',
            f'commands.hidden.{v}',
        ]
        for name in candidates:
            if importlib.util.find_spec(name):
                try:
                    module = importlib.import_module(name)
                    module.execute(self, noun)
                except Exception as e:
                    print(f'Something went wrong: {e}')
                return
        # If no command matched, check if the verb is a named exit from the current room
        if noun is None and self.room is not None:
            room = self.game.getRoom(self.room)
            exits = room.getExits()
            if exits and verb.upper() in exits:
                if not self.game.puzzles.trigger(self, verb.upper(), None, self.room):
                    self.move(verb.upper())
                return
        # Try the puzzle engine — verb may be a known action even without a command file
        if self.game.puzzles.trigger(self, verb.upper(), noun, self.room):
            return
        if self.game.puzzles.has_verb(verb.upper()):
            print('Nothing happens.')
            return
        print(self.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))

    def getCommand(self):
        prompt = self.game.settings.get('input_prompt', 'What do you want to do? ')
        command = input(prompt).upper()
        commands = command.split()
        if len(commands) == 0:
            return
        elif len(commands) == 1:
            self.doCommand(commands[0], None)
        else:
            self.doCommand(commands[0], commands[1])
