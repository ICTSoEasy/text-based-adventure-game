DESCRIPTION = 'stairs - named route'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'STAIRS', None, player.getRoom()):
        print(player.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))
