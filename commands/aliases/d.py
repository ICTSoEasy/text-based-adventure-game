def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'DOWN', None, player.getRoom()):
        player.doCommand('MOVE', 'DOWN')
