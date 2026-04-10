DESCRIPTION = 'UNLOCK - unlock something (e.g. UNLOCK GRATE)'

def execute(player, noun):
    if noun is None:
        print('Unlock what?')
        return
    fired = player.game.puzzles.trigger(player, 'UNLOCK', noun, player.getRoom())
    if not fired:
        print("You can't unlock that.")
