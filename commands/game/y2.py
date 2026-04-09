DESCRIPTION = 'y2 - named route'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'Y2', None, player.getRoom()):
        print(player.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))
