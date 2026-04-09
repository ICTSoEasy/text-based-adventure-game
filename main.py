import curses
import builtins
from GAME import Game
from ROOM import Room
from CREATE import Create
from PLAYER import Player
from TERMINAL import Terminal

def run(stdscr):
    terminal = Terminal(typewriter_speed=0.02)
    terminal.setup(stdscr)

    builtins.print = terminal.game_print
    builtins.input = terminal.game_input

    game = Game()
    Create(game)

    player = Player()
    player.setRoom(15)
    player.setGame(game)
    game.addPlayer(player)

    game.flipPlayStatus()
    while game.getPlayStatus():
        game.tick()

curses.wrapper(run)
