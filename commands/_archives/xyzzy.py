DESCRIPTION = 'XYZZY - magic word'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'XYZZY', None, player.getRoom()):
        print('Nothing happens.')
