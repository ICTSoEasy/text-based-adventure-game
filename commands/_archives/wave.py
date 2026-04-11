DESCRIPTION = 'WAVE - wave an item (e.g. WAVE ROD)'

def execute(player, noun):
    if noun is None:
        print('Wave what?')
        return
    if not player.hasItem(noun):
        print("You aren't carrying it!")
        return
    if not player.game.puzzles.trigger(player, 'WAVE', noun, player.getRoom()):
        print('Nothing happens.')
