DESCRIPTION = "Pick up an item (e.g. GET HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Get what?')
        return
    # Try puzzles first — special-case GET logic (e.g. bird needs cage)
    # If any puzzle fires, it handles the GET entirely
    if player.game.puzzles.trigger(player, 'GET', noun, player.getRoom()):
        return
    player.getItem(noun)
