DESCRIPTION = 'ENTER - enter a nearby location'

def execute(player, noun):
    if not player.game.puzzles.trigger(player, 'ENTER', None, player.getRoom()):
        print(player.game.messages.get('unknown_command', 'Unknown command. Type HELP for help.'))
