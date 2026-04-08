DESCRIPTION = "Pick up an item (e.g. GET HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Get what?')
        return
    player.getItem(noun)
    if player.hasItem(noun):
        player.game.puzzles.trigger(player, 'GET', noun, player.getRoom())
