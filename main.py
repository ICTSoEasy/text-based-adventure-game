#import the classes we have written
from GAME import Game
from ROOM import Room
from CREATE import Create
from PLAYER import Player

#Create (instantiate) an instance of Game, called game
game = Game()
Create(game)

#Create (instantiate) a Player called player
player = Player()
player.setRoom(15)
player.setGame(game)
game.addPlayer(player)

#Run the game
print('running the game')
game.flipPlayStatus()
while game.getPlayStatus():
    game.tick()
print('game ended')
