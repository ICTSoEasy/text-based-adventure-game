DESCRIPTION = "Drop an item you are carrying (e.g. DROP HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Drop what?')
        return
    had_item = player.hasItem(noun) is not None
    player.dropItem(noun)
    if had_item and not player.hasItem(noun):
        player.game.puzzles.trigger(player, 'DROP', noun, player.getRoom())
