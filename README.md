# Python Text Game Engine

A data-driven engine for building text-based games in Python. No programming required to create a game — rooms, items, puzzles, and win conditions are all defined in CSV and JSON files.

Originally conceived as a workshop activity for students, the engine is general-purpose and not limited to adventure games. [Colossal Cave Adventure](#colossal-cave-adventure) is used as a reference implementation to drive engine development.

## For game creators

You can build a complete text-based game by editing four files:

| File | What it controls |
|------|-----------------|
| `rooms.csv` | Rooms, their descriptions, and exits |
| `items.json` | Items, where they start, and their properties |
| `puzzles.json` | All game logic — triggers, conditions, and effects |
| `messages.csv` | All text shown to the player |

No Python knowledge needed. See [`CREATOR.md`](CREATOR.md) for full documentation of every available trigger, condition, and effect.

## For developers

The engine is built around a simple game loop:

- **`main.py`** — entry point and game loop
- **`GAME.py`** — `Game` class: rooms, items, turn counter, scoring
- **`ROOM.py`** — `Room` class: exits, contents, descriptions
- **`PLAYER.py`** — `Player` class: movement, commands, inventory
- **`THING.py`** — `Thing` class: items, state, light, descriptions
- **`PUZZLES.py`** — `PuzzleEngine` class: trigger/condition/effect system
- **`CREATE.py`** — loads world from data files at startup
- **`TERMINAL.py`** — optional status bar support

Game logic lives entirely in `puzzles.json`. The puzzle engine evaluates triggers and conditions on every player command and on every turn (via a `FORCE` verb), then applies effects. This means the Python source rarely needs changing to add new game behaviour.

## Getting started

Requires Python 3.9 or later. No external dependencies.

```bash
git clone https://github.com/ICTSoEasy/text-based-adventure-game.git
cd text-based-adventure-game
python main.py
```

## Colossal Cave Adventure

The `cca-350` branch contains a work-in-progress reimplementation of the classic 1977 [Colossal Cave Adventure](https://en.wikipedia.org/wiki/Colossal_Cave_Adventure) (350-point version). It is implemented entirely through the data files — no changes to the Python engine were made that are specific to CCA.

The implementation is faithful to the original but not 100% identical — some behaviours (particularly the dwarf system and endgame) are not yet implemented, and a small number of puzzle interactions may differ from the original Fortran source.

## Inspiration

- *Write Your Own Adventure Programs* — Jenny Tyler & Les Howarth (Usborne, 1983)
- *Adventure Games in Python* — Oli Howson (ICT So Easy, 2022/2025)

## Credits

Created by **Oli Howson**.

## Licence

[MIT](LICENSE)
