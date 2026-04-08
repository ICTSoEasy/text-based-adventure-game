DESCRIPTION = "Look around, or examine an item (e.g. LOOK or LOOK HAMMER)"

def execute(player, noun):
    if noun is None:
        player.look()
    else:
        player.lookItem(noun)
