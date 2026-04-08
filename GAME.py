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

    #A 'tick' is a round of the game. The game does any
    #house keeping it may need and then gives the player
    #an opportunity to do it's thing.
    def tick(self):
        print('tick')
        self.player.getCommand()
