# Creator's Guide

Everything you need to build your own adventure game. You never need to touch any Python file — all game content lives in CSV files and the `commands/` folder.

---

## File Overview

| File | Purpose |
|------|---------|
| `settings.csv` | Global game configuration |
| `rooms.csv` | Every location in your game |
| `items.csv` | Every object in your game |
| `puzzles.csv` | Triggers, conditions, and effects |
| `messages.csv` | Named text messages (welcome screen etc.) |
| `commands/` | One Python file per verb |

---

## settings.csv

Controls global game behaviour. Format: `setting,value,description`

| Setting | Example | Description |
|---------|---------|-------------|
| `game_name` | `Haunted House` | Name of your game |
| `starting_room` | `1` | Room ID where the player begins |
| `show_exits` | `true` / `false` | Whether to list exits after each LOOK |
| `typewriter_speed` | `0.02` | Seconds per character (0 = instant) |
| `input_prompt` | `What do you want to do? ` | Text shown before each command input (blank for none) |
| `debug` | `true` / `false` | Shows loading detail, tick counter, always shows exits |

**Example:**
```
setting,value,description
game_name,Haunted House,Name of the game
starting_room,1,Starting location
show_exits,true,Show exits after looking
typewriter_speed,0.02,Typewriter effect speed
debug,false,Debug mode
```

---

## rooms.csv

One row per location. Format: `id,short_desc,long_desc,exits`

- **id** — unique number for this room
- **short_desc** — brief name shown in debug/cheat mode
- **long_desc** — full description shown when player LOOKs
- **exits** — pipe-separated list of `DIRECTION:room_id` pairs, or blank for no exits

Valid directions: `NORTH`, `SOUTH`, `EAST`, `WEST`, `NE`, `SE`, `SW`, `NW`, `UP`, `DOWN`

**Example:**
```
id,short_desc,long_desc,exits
1,Dark Hallway,You are standing in a dark hallway. Cobwebs hang from the ceiling.,NORTH:2|EAST:3
2,Kitchen,A dusty kitchen. The smell of something old hangs in the air.,SOUTH:1
3,Library,Floor-to-ceiling bookshelves line every wall.,WEST:1
```

**Tips:**
- Rooms with no exits (blank) are dead ends — the player will be trapped unless a puzzle adds an exit
- Exits can be one-way (room 1 goes NORTH to room 2, but room 2 may not go SOUTH back)
- You can add and remove exits dynamically using puzzles

---

## items.csv

One row per object. Format: `id,short_desc,long_desc,gettable,room_id`

- **id** — unique number for this item
- **short_desc** — name used in commands (e.g. `GET HAMMER` matches `hammer`)
- **long_desc** — description shown when player LOOKs at the item
- **gettable** — `true` if the player can pick it up; `false` for fixed objects
- **room_id** — which room the item starts in

**Example:**
```
id,short_desc,long_desc,gettable,room_id
1,hammer,A heavy iron hammer with a worn wooden handle.,true,1
2,anvil,A massive iron anvil. You couldn't possibly lift it.,false,2
3,key,A small brass key.,true,3
```

---

## messages.csv

Named text messages used throughout the game. Format: `id,text`

The `welcome` message (if present) is shown automatically when the game starts.

**Escape sequences and magic commands:**

| Sequence | Result |
|----------|--------|
| `\n` | New line |
| `{sp:4}` | 4 spaces (use any number) |

**Example:**
```
id,text
welcome,{sp:8}WELCOME TO HAUNTED HOUSE\n\nCan you find the treasure and escape?
hint,Have you tried looking at everything in the room?
```

To display a message from a puzzle, use the `PRINT_MSG` effect (see puzzles below).

---

## puzzles.csv

The puzzle engine connects player actions to game events. Each row is one effect. A single puzzle can span multiple rows (they all fire together).

### Columns

| Column | Description |
|--------|-------------|
| `trigger_verb` | Verb that activates this row (`USE`, `MOVE`, `GET`, `DROP`, or blank for any) |
| `trigger_item` | Item name that must be used (or blank for any) |
| `trigger_room` | Room ID where this triggers (or blank for any room) |
| `condition_item` | Player must be carrying this item |
| `condition_not_item` | Player must NOT be carrying this item |
| `condition_room_item` | This item must be present in the current room |
| `effect_type` | What happens (see below) |
| `effect_target` | What the effect acts on |
| `effect_value` | Value for the effect |
| `message` | Text to display when this fires |
| `delay` | Seconds to pause before this effect (for dramatic timing) |
| `once` | `true` = fire only once ever; `false` = fire every time |

### Effect Types

| Effect | Target | Value | Description |
|--------|--------|-------|-------------|
| `PRINT_MSG` | *(blank)* | *(blank)* | Display the `message` column text |
| `ADD_EXIT` | room id | `DIRECTION:room_id` | Add an exit to a room |
| `REMOVE_EXIT` | room id | `DIRECTION` | Remove an exit from a room |
| `SET_ROOM_DESC` | room id | new description | Change a room's long description |
| `SET_ITEM_SHORT_DESC` | item name | new short desc | Change an item's short (command) name |
| `SET_ITEM_LONG_DESC` | item name | new long desc | Change an item's description |
| `WIN` | *(blank)* | *(blank)* | End the game with a win |
| `LOSE` | *(blank)* | *(blank)* | Kill the player |

### Example: Unlock a door with a key

```
trigger_verb,trigger_item,trigger_room,condition_item,condition_not_item,condition_room_item,effect_type,effect_target,effect_value,message,delay,once
USE,KEY,1,,,DOOR,PRINT_MSG,,,You unlock the door with the key.,0,true
USE,KEY,1,,,DOOR,ADD_EXIT,1,NORTH:2,,0,true
USE,KEY,1,,,DOOR,SET_ROOM_DESC,1,The hallway. The door to the north is now open.,,0,true
```

### Example: Win condition

```
MOVE,,2,COIN,,,PRINT_MSG,,,You place the coin in the fountain. A golden light surrounds you...,2,false
MOVE,,2,COIN,,,WIN,,,YOU WIN!,0,false
```

### Example: Death trap

```
MOVE,,5,,,,PRINT_MSG,,,The floor gives way!,2,false
MOVE,,5,,,,LOSE,,,,0,false
```

### Example: Transform an item

```
USE,KNIFE,,,,ROPE,SET_ITEM_SHORT_DESC,ROPE,scraps,,0,true
USE,KNIFE,,,,ROPE,SET_ITEM_LONG_DESC,ROPE,Tattered scraps of rope. Useless now.,,0,true
USE,KNIFE,,,,ROPE,PRINT_MSG,,,You cut the rope into useless scraps.,0,true
```

---

## commands/ folder

Each verb the player can type is a separate Python file in `commands/`. To add a new command, create a file named `commands/yourverb.py` with this structure:

```python
DESCRIPTION = 'YOURVERB - brief description shown in HELP'

def execute(player, noun):
    print('Your command logic here')
```

The `HELP` command automatically discovers all files in this folder and lists their `DESCRIPTION`.

Built-in commands: `LOOK`, `GET`, `DROP`, `USE`, `MOVE`, `ITEMS`, `HELP`, `CHEAT`, `FAST`

---

## Tips for designing your game

1. **Draw your map first** — number your rooms on paper before touching the CSV
2. **Start small** — get a 5-room loop working before adding puzzles
3. **Test often** — set `debug,true` in settings to see what's happening
4. **One-way exits are valid** — useful for slides, drops, or dramatic moments
5. **Puzzles fire in order** — if multiple rows match, they all fire top-to-bottom
6. **`once,true`** — use this for anything that should only happen once (unlocking a door, breaking a wall)
7. **`once,false`** — use for repeating events (a slippery floor, a recurring message)
8. **Items as keys** — `condition_item` and `condition_not_item` let you gate puzzles on inventory
