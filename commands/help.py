DESCRIPTION = "Show available commands"

import os
import importlib

def execute(player, noun):
    print('Commands:')
    commands_dir = os.path.dirname(__file__)
    for filename in sorted(os.listdir(commands_dir)):
        if filename.endswith('.py') and not filename.startswith('_'):
            verb = filename[:-3].upper()
            try:
                mod = importlib.import_module(f'commands.{filename[:-3]}')
                desc = getattr(mod, 'DESCRIPTION', '')
                print(f'  {verb}: {desc}')
            except Exception:
                pass
