def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'UP', None, player.getRoom()):
        player.doCommand('MOVE', 'UP')
