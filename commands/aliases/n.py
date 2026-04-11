def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'NORTH', None, player.getRoom()):
        player.doCommand('MOVE', 'NORTH')
