def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'SE', None, player.getRoom()):
        player.doCommand('MOVE', 'SE')
