DESCRIPTION = 'PLUGH - magic word'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'PLUGH', None, player.getRoom()):
        print('A hollow voice says "PLUGH".')
