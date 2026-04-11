def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'WEST', None, player.getRoom()):
        player.doCommand('MOVE', 'WEST')
