#An initial definition of the game
class Game:
    #Initiaslisation happens when you take this description and make it into
    #an object.
    # - self - all class definitions need this so that it can look at
    #   it's own properties & methods
    # - rooms will be the dictionary of rooms - these will start as empty
    # - items will be the dictionary of items not held in a room - these will start as empty
    def __init__(self):
        self.rooms = {} #empty list
        self.items = {} #empty list
        self.status = False #not in play
        self.player = None #No player until we add them
        self.puzzles = None #Puzzle engine, set up in CREATE
        self.turn_counter = 0
        self.score = 0

    #This will tell us whether we are in play or not
    def getPlayStatus(self):
        return self.status

    #This will invert the play status (if we are playing, make us not playing and vice versa)
    def flipPlayStatus(self):
        self.status = not self.status

    #This will add an object to the items dictionary
    def addItem(self,room,item):
        self.rooms[room].putIn(item)

    #This will add a room to the rooms list
    #It stores it under it's own ID for ease of access
    def addRoom(self,room):
        self.rooms[room.getId()] = room

    #This will list all rooms currently 'owned' by the game
    # not useful for the player, but good for our debugging.
    def listRooms(self):
        print('Listing rooms')
        print('=============')
        for id in self.rooms:
            print(id, '->', self.rooms[id].getShortDesc())

    #This will add a long description to a given room
    def addRoomLongDescription(self,room,desc):
        self.rooms[room].setLongDesc(desc)

    #This will add the player to the game
    def addPlayer(self,player):
        self.player = player

    #This will take an id, and return the room object with that id
    def getRoom(self,id):
        return self.rooms[id]

    #Find an item by name (uppercase) across all rooms and player inventory
    def findItem(self, name):
        name = name.upper()
        for room in self.rooms.values():
            item = room.ifContains(name)
            if item:
                return item
        if self.player:
            item = self.player.hasItem(name)
            if item:
                return item
        return None

    #Find ALL items matching a name across all rooms and player inventory
    def findAllItems(self, name):
        name = name.upper()
        found = []
        for room in self.rooms.values():
            for item in room.getContains():
                if item.matchesName(name):
                    found.append(item)
        if self.player:
            for item in self.player.items:
                if item.matchesName(name):
                    found.append(item)
        return found

    #A 'tick' is a round of the game. The game does any
    #house keeping it may need and then gives the player
    #an opportunity to do it's thing.
    def tick(self):
        if getattr(self, 'settings', {}).get('debug', False):
            print(f'[tick]')
        if self.puzzles:
            self.puzzles.trigger(self.player, 'FORCE', None, self.player.getRoom())
        if self.status:
            self.player.getCommand()
            self.turn_counter += 1
            self.decrement_lights()
            if self.settings.get('debug', False):
                print(f'  [turn {self.turn_counter}]')
            self._update_status()

    def decrement_lights(self):
        debug = self.settings.get('debug', False)
        all_items = []
        for room in self.rooms.values():
            all_items.extend(room.getContains())
        if self.player:
            all_items.extend(self.player.items)

        for item in all_items:
            if item.getLightTurns() > 0:
                if item.getMakingLight():
                    item.decrementLight()
                if debug:
                    print(f'  [light] {item.getShortDesc()}: making_light={item.getMakingLight()} turns_remaining={item.getTurnsRemaining()}')

    def _update_status(self):
        import TERMINAL
        t = TERMINAL.get()
        if not t:
            return
        name = self.settings.get('game_name', '')
        score = self.score if self.settings.get('show_score', True) else None
        turns = self.turn_counter if self.settings.get('show_turns', True) else None
        t.update_status(name, score, turns)
