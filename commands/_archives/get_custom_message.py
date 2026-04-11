# Archive: custom GET success message
# Original version said "You manage to get a {short_desc}" instead of the
# Colossal Cave Adventure's plain "OK". Preserved here in case you prefer it.
#
# To restore: replace the print('OK') in PLAYER.py getItem() with:
#     print('You manage to get a', thing.getShortDesc())

DESCRIPTION = "Pick up an item (e.g. GET HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Get what?')
        return
    if player.game.puzzles.trigger(player, 'GET', noun, player.getRoom()):
        return
    player.getItem(noun)
