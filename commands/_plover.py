def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'PLOVER', None, player.getRoom()):
        print('Nothing happens.')
