def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'EAST', None, player.getRoom()):
        player.doCommand('MOVE', 'EAST')
