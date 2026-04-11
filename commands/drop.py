DESCRIPTION = "Drop an item you are carrying (e.g. DROP HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Drop what?')
        return
    if not player.hasItem(noun):
        print('You do not have a', noun.lower(), 'to drop!')
        return
    if player.game.puzzles.trigger(player, 'DROP', noun, player.getRoom()):
        return
    player.dropItem(noun)
