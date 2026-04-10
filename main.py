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

    terminal.typewriter_speed = game.settings.get('typewriter_speed', 0.02)

    player = Player()
    player.setRoom(game.settings.get('starting_room', 1))
    player.setGame(game)
    game.addPlayer(player)

    game._update_status()

    if 'welcome' in game.messages:
        print(game.messages['welcome'])

    game.flipPlayStatus()
    while game.getPlayStatus():
        game.tick()

curses.wrapper(run)
