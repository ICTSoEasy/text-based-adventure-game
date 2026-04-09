DESCRIPTION = 'YES - affirmative response'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'YES', None, player.getRoom()):
        print('OK.')

