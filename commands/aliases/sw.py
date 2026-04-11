def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'SW', None, player.getRoom()):
        player.doCommand('MOVE', 'SW')
