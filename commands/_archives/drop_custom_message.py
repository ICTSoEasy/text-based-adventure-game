# Archive: custom DROP success message
# Original version said "You drop a {noun}" instead of the
# Colossal Cave Adventure's plain "OK". Preserved here in case you prefer it.
#
# To restore: replace the print('OK') in PLAYER.py dropItem() with:
#     print('You drop a', noun.lower())

DESCRIPTION = "Drop an item you are carrying (e.g. DROP HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Drop what?')
        return
    had_item = player.hasItem(noun) is not None
    player.dropItem(noun)
    if had_item and not player.hasItem(noun):
        player.game.puzzles.trigger(player, 'DROP', noun, player.getRoom())
