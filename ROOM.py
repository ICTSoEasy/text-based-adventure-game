#An initial definition of a room
class Room:
    #Initiiaslisation happens when you take this description and make it into
    #an object.
    # - self - all class definitions need this so that it can look at
    #   it's own properties & methods
    # - id - we will give it a number to identify itt by
    # - shortDesc will be the 'name' of the room
    # - exits will be a list of exits from the room
    # - contains will be a list of the things contained in the room
    # - longDesc will be the longer description which we will only see if we actually look around.
    #   as this is not strictly necessary, we start it as nothing and then set it later if we
    #   so wish.
    def __init__(self, id, shortDesc, exits, contains, lit=False):
        self.id = id
        self.shortDesc = shortDesc
        self.exits = exits
        self.contains = contains
        self.longDesc = ''
        self.lit = lit

    def isLit(self):
        return self.lit

    #This will look at itself and give us back the ID
    def getId(self):
        return self.id #just give back whatever the ID is

    #This will look at itself and give us back the short description
    def getShortDesc(self):
        return self.shortDesc #just give back whatever the current short description is

    #This will take the new description we give it and set this as the object's short description
    def setShortDesc(self,desc):
        self.shortDesc = desc

    #This will look at itself and give us back the long description
    def getLongDesc(self):
        return self.longDesc #Just give back whatever the current long desc is

    #This will take the new description we give it and set this as the object's long description
    def setLongDesc(self,desc):
        self.longDesc = desc

    #This give us a list of exits
    def getExits(self):
        return self.exits

    #This allows us to add a new exit direction which points to the ID of whatever room we wish
    def addExit(self,exitDirection,exitID):
        if self.exits is None:
            self.exits = {}
        self.exits.update({exitDirection:exitID})

    #This allows us to remove an exit direction
    def removeExit(self,exitDirection):
        if exitDirection in self.exits:
            del self.exits[exitDirection]

    #This will give us a list of things the room contains
    def getContains(self):
        return self.contains

    #This will let us test if a particular item is in the room
    def ifContains(self, lookingFor):
        for item in self.getContains():
            if item.matchesName(lookingFor):
                return item
        return None

    #This lets us remove an item from the room
    def remove(self,item):
        self.contains.remove(item)

    #This lets us put an item in to the room
    def putIn(self,item):
        self.contains.append(item)
