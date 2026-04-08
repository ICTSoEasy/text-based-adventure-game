DESCRIPTION = "Move in a direction (e.g. MOVE NORTH)"

def execute(player, noun):
    if noun is None:
        print('Move where? (e.g. MOVE NORTH)')
        return
    moved = player.move(noun)
    if moved:
        player.game.puzzles.trigger(player, 'MOVE', None, player.getRoom())
