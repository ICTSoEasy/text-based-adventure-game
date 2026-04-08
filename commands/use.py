DESCRIPTION = "Use an item you are carrying (e.g. USE HAMMER)"

def execute(player, noun):
    if noun is None:
        print('Use what?')
        return
    if not player.hasItem(noun):
        print('You do not have a', noun.lower())
        return
    fired = player.game.puzzles.trigger(player, 'USE', noun, player.getRoom())
    if not fired:
        print('You think about using a', noun.lower() + ', but this does not seem like the right kind of place to do so.')
