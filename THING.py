#An initial definition of a thing
class Thing:
    def __init__(self, id, shortDesc, longDesc, gettable=True, idWords=None, roomDescs=None, state=0):
        self.id = id
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.gettable = gettable
        self.idWords = idWords or [shortDesc.upper()]
        self.roomDescs = roomDescs or []
        self.state = state
        self.making_light = 0
        self.light_turns = 0
        self.turns_remaining = 0

    def getMakingLight(self):
        return self.making_light

    def setMakingLight(self, value):
        self.making_light = value

    def getLightTurns(self):
        return self.light_turns

    def setLightTurns(self, value):
        self.light_turns = value
        self.turns_remaining = value

    def getTurnsRemaining(self):
        return self.turns_remaining

    def decrementLight(self):
        if self.turns_remaining > 0:
            self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            self.making_light = 0
            self.state = 0

    #This will look at itself and give us back the ID
    def getId(self):
        return self.id #just give back whatever the ID is

    #This will look at itself and give us back the short description
    def getShortDesc(self):
        return self.shortDesc #just give back whatever the current short description is

    #This will take the new description we give it and set this as the
    #object's short description
    def setShortDesc(self,desc):
        self.shortDesc = desc

    #This will look at itself and give us back the long description
    def getLongDesc(self):
        return self.longDesc #Just give back whatever the current long desc is

    #This will take the new description we give it and set this as the
    #object's long description
    def setLongDesc(self,desc):
        self.longDesc = desc

    def matchesName(self, word):
        return word.upper() in self.idWords

    def getRoomDesc(self):
        if self.roomDescs and self.state < len(self.roomDescs):
            return self.roomDescs[self.state]
        return ''

    def setState(self, state):
        self.state = state

    #This will toggle the gettability of the thing
    def toggleGettable(self):
        self.gettable = not self.gettable

    #This will return weather a thing can be got
    def isGettable(self):
        return self.gettable
