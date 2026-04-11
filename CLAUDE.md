# Project Memory

## Preferences
- Use CLAUDE.md (this file) for all memory instead of the file-based memory system under ~/.claude/projects/
- Do not add content (examples, documentation body, code) unless explicitly asked. If asked to add a section or heading, add only the heading and let the user fill it in.
- Do not do things without being asked — complete the stated task only.
- All in-game messages must be identical to the original Colossal Cave Adventure. If there is any reason a message must vary from the original, ask before changing it.
- When asked to commit, always push immediately after.

## Project Overview
A Python text-based adventure game built as a **workshop activity** — the goal is for students/participants to create their own adventures without writing Python code, by editing CSV files.

### Inspiration Chain
- **1983 Usborne book**: *Write Your Own Adventure Programs* (Jenny Tyler & Les Howarth) — original inspiration. Teaches adventure game concepts using BASIC. Example game: *Haunted House* (64 locations, grid-based, treasures, puzzles, two-word commands). Key concepts: locations on a numbered grid, compass directions + up/down, objects/props, one-way routes, scoring, verb+noun commands.
- **ICT So Easy Book 7**: *Adventure Games in Python* (Oli's book, 2022/2025) — Python/OOP reimplementation of those ideas. Example game: *Drop the Hook* — pirate ship, 23 rooms, player starts on Poop Deck, must reach Starboard Bows with a coin to win. Shark trap in room 23 (Rudder).

### Architecture
- `main.py` — entry point, game loop
- `GAME.py` — Game class (rooms, player, tick)
- `ROOM.py` — Room class (id, short/long desc, exits dict, contains list)
- `PLAYER.py` — Player class (all commands: LOOK, MOVE, GET, DROP, USE, ITEMS, CHEAT, HELP)
- `THING.py` — Thing class (id, short/long desc, gettable flag)
- `CREATE.py` — loads world from CSV files
- `rooms.csv` — room data (exits as `DIRECTION:id|DIRECTION:id`)
- `items.csv` — item data (gettable True/False, room_id for placement)

### Git Structure
- `main` branch — clean book version (tagged `v1.0-book-original`)
- `workshop` branch — new version under development (current)

### Workshop Design Goal
Students should only need to edit `rooms.csv` and `items.csv` to build their own adventure. The Python files should handle everything else, including any puzzle/win logic — the question of how to make puzzles/win conditions data-driven (vs hardcoded in PLAYER.py) is still to be solved.
