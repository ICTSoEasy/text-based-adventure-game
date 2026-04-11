def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'NW', None, player.getRoom()):
        player.doCommand('MOVE', 'NW')
