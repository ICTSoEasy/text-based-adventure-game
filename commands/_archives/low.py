DESCRIPTION = 'low - named route'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'LOW', None, player.getRoom()):
        print(player.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))
