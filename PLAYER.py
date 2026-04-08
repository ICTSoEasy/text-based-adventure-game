import time
import random
#An initial definition of a player
class Player:
    #Initialisation happens when you take this description and make it into
    #an object.
    # - self - all class definitions need this so that it can look at
    #   it's own properties & methods
    def __init__(self):
        self.alive = True
        self.room = None
        self.items = [] #Changed to [] instead of {}
        self.game = None

    def setGame(self,game):
        self.game = game

    def isAlive(self):
        return self.alive

    def kill(self):
        self.alive = False
        print('Oh no. You appear to be dead!')
        anotherGo = input('Want another go? (y/n)').upper()
        if anotherGo == 'Y':
            print('You magically un-ghost. I wonder where your body will end up?')
            roomNumber = -1
            while roomNumber not in [23,9]:
                roomNumber = random.randint(1,23)
            self.setRoom(12)
            self.resuscitate()
        else:
            self.game.flipPlayStatus()

    def resuscitate(self):
        self.alive = True

    def setRoom(self,room):
        self.room = room

    def getRoom(self):
        return self.room

    def look(self):
        room = self.game.getRoom(self.getRoom())
        print(room.getLongDesc())
        for thing in room.getContains():
            print('A',thing.getShortDesc(),'is here.')
        try:
            exits = room.getExits()
            keys = ', '.join(exits.keys())
        except:
            keys = "None!"
        print('Exits: '+keys)

    def lookItem(self,noun):
        found = False
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing != None:
            print(thing.getLongDesc())
            found = True
        thing = self.hasItem(noun)
        if thing != None:
            print(thing.getLongDesc())
            found = True
        if not found:
            print('I cannot find one of them!')

    #This will let us test if a particular item is held
    #It is very similar to the room code!
    def hasItem(self,lookingFor):
        items = self.items
        for item in items:
            if item.getShortDesc().upper() == lookingFor:
                return item
        return None

    def getItem(self,noun):
        room = self.game.getRoom(self.getRoom())
        thing = room.ifContains(noun)
        if thing != None:
            self.items.append(thing)
            room.remove(thing)
            print('You manage to get a',noun.lower())
            if not thing.isGettable():
                print('Uh-oh... you struggle to hold a',noun.lower())
                self.dropItem(noun)
        else:
            print('You cannot find a',noun.lower())

    def dropItem(self,noun):
        room = self.game.getRoom(self.getRoom())
        thing = self.hasItem(noun)
        if thing != None:
            room.putIn(thing)
            self.items.remove(thing)
            print('You drop a',noun.lower())
        else:
            print('You do not have a',noun.lower(),'to drop!')

    def useItem(self,item):
        if not self.hasItem(item):
            print('You do not have a',item.lower())
        elif item == "KNIFE" and self.game.getRoom(self.getRoom()).ifContains('SACKS'):
            thing = self.game.getRoom(self.getRoom()).ifContains('SACKS')
            print("The sacks disintegrate into scraps. There was nothing in them after all!")
            thing.setShortDesc("scraps")
            thing.setLongDesc("scraps of cloth that may once have been sacks.")
        elif item == "HAMMER" and self.getRoom() == 9:
            print('hurrah!')
            room = self.game.getRoom(self.getRoom())
            if room.getExits() == {}:
                print('You bash away at the wall with your hammer')
                time.sleep(2)
                print('The wall comes down!')
                room.addExit('NORTH',8)
                room.setLongDesc("The port midships is the port side of the middle of the ship. The foremast and mainast stretch way, way, way above you. A rough hole has been based in the North wall.")
                room = self.game.getRoom(8)
                room.addExit('SOUTH',9)
                room.setLongDesc("The starboard midships is the starboard side of the middle of the ship, smack between the main mast and the foremast. Just ripe for anything falling from the masts to land on your noggin. A rough hole has been bashed in the South wall.")
        #Else is using something you have, but it does nothing.
        else:
            print('You think about using a',item.lower(),'but this does not seem like the right kind of place to do so.')

    def move(self,direction):
        room = self.game.getRoom(self.getRoom())
        exits = room.getExits()
        if direction in exits.keys():
            print('\nYou move.\n')
            self.room = exits[direction]
            self.look()
        else:
            print('I cannot move that way')
        if self.room == 23:
            time.sleep(2)
            print('In fact... it is *really* slippy here!')
            time.sleep(2)
            print('A bit ... tooo.... slippppppyyy......')
            time.sleep(2)
            print('SPLASH!')
            time.sleep(2)
            print('What is that triangle in the water?')
            time.sleep(2)
            print('CHOMP!!')
            self.kill()
        elif self.room == 1:
            if self.hasItem("COIN"):
                print('You ponder')
                time.sleep(2)
                print('You reach into your pocket and pull out the golden coin.')
                time.sleep(2)
                print('You flick the coin in the air and... WHIZZZZZZ!')
                time.sleep(2)
                print('You find yourself teleported to the nicest of pirate islands, surrounded by gold and rum and ... gold...')
                time.sleep(2)
                print('YOU WIN! Well done :)')
                self.game.flipPlayStatus()
            else:
                print("This feels like a really opportune kind of place. You're just sure that with a little money in your pocket you could really make something of yourself from here.")

    def listItems(self):
        count = 0
        print('Things you are holding:')
        for item in self.items:
            print('-',item.getShortDesc())
            count += 1
        if count == 0:
            print('- Nothing!')

    def doCommand(self,verb,noun):
        if verb == 'HELP':
            self.help()
        elif verb == 'LOOK':
            if noun == None:
                self.look()
            else:
                self.lookItem(noun)
        elif verb == 'MOVE':
            self.move(noun)
        elif verb == 'GET':
            self.getItem(noun)
        elif verb == 'DROP':
            self.dropItem(noun)
        elif verb == 'USE':
            self.useItem(noun)
        elif verb == 'CHEAT':
            self.room = int(noun)
        elif verb == 'ITEMS':
            self.listItems()
        else:
            print('Unknown verb or noun...')

    def help(self):
        print('Commands:')
        print('LOOK: Look around the current room.')
        print('LOOK <item>: Looks at a specified item.')
        print('MOVE <direction>: Move in the given direction')
        print('GET <item>: Tries to pick up an item.')
        print('DROP <item>: Tries to drop an item.')
        print('USE <item>: Tries to use an item.')
        print('ITEMS: Lists the items you are carrying.')

    def getCommand(self):
        command = input('What do you want to do? ').upper()
        commands = command.split(' ')
        while True:
            if len(commands) == 1:
                verb = commands[0]
                self.doCommand(verb,None)
                break
            elif len(commands) == 2:
                verb = commands[0]
                noun = commands[1]
                self.doCommand(verb,noun)
                break
            else:
                print('Please enter a verb followed by an optional noun.')
                print('Enter HELP for help.')
