def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'PLUGH', None, player.getRoom()):
        print('Nothing happens.')
