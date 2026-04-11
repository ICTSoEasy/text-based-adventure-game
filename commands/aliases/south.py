def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'SOUTH', None, player.getRoom()):
        player.doCommand('MOVE', 'SOUTH')
