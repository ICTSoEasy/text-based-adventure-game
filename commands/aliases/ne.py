def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'NE', None, player.getRoom()):
        player.doCommand('MOVE', 'NE')
