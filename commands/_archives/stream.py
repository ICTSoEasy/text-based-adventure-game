DESCRIPTION = 'stream - named route (CCA)'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'STREAM', None, player.getRoom()):
        print(player.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))
