# Creator's Guide

Everything you need to build your own adventure game. You never need to touch any Python file — all game content lives in CSV files and the `commands/` folder.

---

## File Overview

| File | Purpose |
|------|---------|
| `settings.csv` | Global game configuration |
| `rooms.csv` | Every location in your game |
| `items.json` | Every object in your game |
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
| `use_uppercase` | `true` / `false` | Convert all game output to uppercase (original 1977 style) |

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

## items.json

One object per JSON entry. Fields:

- **id** — unique number for this item
- **id_words** — list of words the player can use to refer to this item (e.g. `["hammer", "hamme"]` means both `GET HAMMER` and `GET HAMME` work). If omitted, defaults to `short_desc`
- **short_desc** — fallback name shown in room if `room_desc` is empty (e.g. `A hammer is here.`)
- **long_desc** — description shown when player does `LOOK HAMMER`. Omit to show the default "not allowed to give more detail" message
- **room_desc** — list of descriptions shown when item is present in a room. Multiple entries correspond to item states (e.g. `["The lamp is unlit.", "The lamp is glowing brightly."]`). If omitted, falls back to `A {short_desc} is here.`
- **gettable** — `true` if the player can pick it up; `false` for fixed objects. Defaults to `true`
- **room_id** — which room the item starts in
- **state** — which `room_desc` to display (0-indexed). Defaults to `0`. Change via puzzles to show a different description

You can add `{"_comment": "=== Section heading ==="}` entries to organise the file — the engine ignores them.

**Example:**
```json
[
  {"_comment": "=== TOOLS (room 1) ==="},
  {"id": 1, "id_words": ["hammer", "hamme"], "short_desc": "hammer", "long_desc": "A heavy iron hammer.", "room_desc": ["A hammer lies on the floor."], "gettable": true, "room_id": 1},
  {"id": 2, "id_words": ["anvil"], "short_desc": "anvil", "long_desc": "A massive iron anvil. You couldn't possibly lift it.", "gettable": false, "room_id": 2},
  {"id": 3, "id_words": ["key"], "short_desc": "key", "room_desc": ["There is a small brass key here.", "The key has been used."], "gettable": true, "room_id": 3}
]
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

To display a message from a puzzle, add `message_file` to any puzzle row (see puzzles below).

---

## puzzles.csv

The puzzle engine connects player actions to game events. Each row is one effect. A single puzzle can span multiple rows (they all fire together).

### Columns

| Column | Description |
|--------|-------------|
| `trigger_verb` | Verb that activates this row (`USE`, `MOVE`, `GET`, `DROP`, compass directions `NORTH`/`SOUTH`/`EAST`/`WEST`/`NE`/`NW`/`SE`/`SW`/`UP`/`DOWN`, or blank for any). Compass direction triggers fire **before** movement — if any row fires, the movement is cancelled. |
| `trigger_item` | Item noun that must be used (or blank for any). Comma-separated to accept multiple. Use `OIL>BOTTLE` to match typed word OIL but check BOTTLE exists; use `>BOTTLE` to match a bare verb (no noun) but check BOTTLE exists |
| `trigger_room` | Room ID where this triggers (or blank for any room) |
| `condition_item` | Player must be carrying this item |
| `condition_not_item` | Player must NOT be carrying this item |
| `condition_room_item` | This item must be present in the current room |
| `condition_not_room_item` | This item must NOT be present in the current room (comma-separated for multiple) |
| `condition_item_state` | `item_name:state` — named item must be in this state (e.g. `grate:0`). Blank = any state |
| `condition_item_turns_eq` | `item_name:value` — named item's turns remaining must equal value (e.g. `lamp:50`). Fires on exactly that turn. Blank = no check |
| `condition_location_dark` | `true` = only fire when the player's location is dark; `false` = only fire when lit. Blank = either |
| `condition_counter_gte` | `counter_name:value` — named counter must be ≥ value (e.g. `dark_moves:2`). Blank = no check |
| `condition_counter_is` | `counter_name:value` — named counter must equal this value exactly. Blank = no check |
| `condition_counter_not` | `counter_name:value` — named counter must NOT equal this value. Blank = no check |
| `condition_counter_exists` | `counter_name` — named counter must exist (has been set at least once) |
| `effect_type` | What happens (see below). Can be omitted if you only want to print a message |
| `effect_target` | What the effect acts on. Use the special value `TRIGGER_ITEM` to act on whatever item the player typed (e.g. to destroy whichever treasure was thrown) |
| `effect_value` | Value for the effect |
| `message` | Text to print when this row fires — printed before the effect runs. Can be added to any effect type, not just `PRINT_MSG`. Takes priority over `message_file` |
| `message_file` | ID of a message in `messages.csv` to print when this row fires. Used if `message` is blank. Can be added to any effect type |
| `delay` | Seconds to pause before this effect (for dramatic timing) |
| `once` | `true` = fire only once ever; `false` = fire every time |
| `chance_pct` | Integer 1–100. If set, the row only fires that percentage of the time (e.g. `35` = 35% chance). Blank = always fires |

### Effect Types

| Effect | Target | Value | Description |
|--------|--------|-------|-------------|
| `PRINT_MSG` | *(blank)* | *(blank)* | Print a message with no other effect. Equivalent to omitting `effect_type` and using `message` |
| `PRINT_MSG_FILE` | message id | *(blank)* | Print a named message with no other effect. Equivalent to omitting `effect_type` and using `message_file` |
| `TELEPORT` | *(blank)* | room id | Move the player to a room and show its description |
| `ADD_EXIT` | room id | `DIRECTION:room_id` — comma-separated for multiple (e.g. `OVER:27,EAST:27`) | Add one or more exits to a room |
| `REMOVE_EXIT` | room id | `DIRECTION` — comma-separated for multiple | Remove one or more exits from a room |
| `SET_ROOM_LONG_DESC` | room id | new description | Change a room's long description |
| `SHOW_ROOM_LONG_DESC` | room id (or blank for current room) | *(blank)* | Print a room's long description |
| `SET_ITEM_STATE` | item name | state number | Set the state of all items with that name (controls which `room_desc` is shown) |
| `SET_ITEM_SHORT_DESC` | item name | new short desc | Change an item's short (command) name |
| `SET_ITEM_LONG_DESC` | item name | new long desc | Change an item's description |
| `START_COUNTER` | counter name | starting value | Set a named counter to a specific value (creates it if it doesn't exist) |
| `INC_COUNTER` | counter name | amount (default 1) | Add a specific amount to a named counter (default 1) |
| `DEC_COUNTER` | counter name | amount (default 1) | Subtract a specific amount from a named counter |
| `RESET_COUNTER` | counter name | *(blank)* | Reset a named counter to 0 |
| `DESTROY_ITEM` | item name | *(blank)* | Remove an item from the game entirely, wherever it is (room or player inventory) |
| `HIDE_ITEM` | item name | *(blank)* | Remove an item from play temporarily (not destroyed — can be brought back with `SHOW_ITEM`) |
| `SHOW_ITEM` | item name | room id (blank = current room) | Bring a hidden item back into play in the specified room |
| `CREATE_ITEM` | item name | room id (blank = current room) | Bring an unborn item into the world, placing it in the specified room |
| `WIN` | *(blank)* | *(blank)* | End the game with a win |
| `LOSE` | *(blank)* | *(blank)* | Kill the player |

See the **Example Puzzles** section at the end of this guide for full worked examples.

---

## commands/ folder

Each verb the player can type is a separate Python file in `commands/`. To add a new command, create a file named `commands/yourverb.py` with this structure:

```python
DESCRIPTION = 'YOURVERB - brief description shown in HELP'

def execute(player, noun):
    print('Your command logic here')
```

The `HELP` command automatically discovers all files in this folder and lists their `DESCRIPTION`.

Built-in commands: `LOOK`, `GET`, `DROP`, `UNLOCK`, `OPEN`, `MOVE`, `ITEMS`, `HELP`, `CHEAT`, `DEBUG`, `FAST`

Hidden commands (not shown in HELP): `CHEAT`, `DEBUG`

---

---

## Example Puzzles

### Opening a passageway with a found item
A common problem is to have a locked or blocked passageway that needs to be opened or unlocked with a found item. 

__Adventure example:__ There is a grate in rooms 8/9 that is locked and needs to be _unlocked_ with keys from room 3.

1. Add the needed item. In this case, it's a key (actually a set of keys). Add an _item_ with id_words set to "keys" (I actually set to key _and_ keys using `key,keys` to allow either). The short description is what will be used when you "get" them. Note this is a variation from the original game which just says "OK". If you want to be able to "look" a the item, give it a long_desc. Adventure doesn't generally do this so it can be left blank for a default message. The _room_desc_ is what is seen when the player enters or looks in the room. _There are some keys on the ground here._ is good enough. The item needs to be able to be picked up, so set _gettable_ to TRUE. Set the id the item will be in, and by default set the state to 0.

2. Create the passageway items. In our example, it's a grating. You need an item for *each end* of the passageway (because who says it can only have two ends?) Each one should have a different ID - this could be as simple as "3" and "4" - I actually used "3" and "1003" so as not to interfere with the original game IDs. ID words I set to "grate" along with the short description. No long description needed if you don't want. Now the bit that makes it fun, the _room_desc_. The grate is a bit different to the keys in that the description will change based on whether it's open or shut. We separate the two descriptions with a | pipe: _THE GRATE IS LOCKED.|THE GRATE IS OPEN._ - the first one aligns to state 0 which is our normal starting state. _gettable_ is FALSE (we don't want people nicking our gratings), the room ID(s) need to be set, and state starts off as 0. Note in the Adventure example, the _only_ things that vary on the two rows are the ID and the room_id. 

3. Create the command. This is fairly commonplace code - you can copy almost any existing verb-noun pair. The terminology we're looking for will be _UNLOCK GATE_ - so we create a file `unlock.py` for the verb in our `commands/game` directory. The only things we need to change are:
- Description - this pushes through to help (and is ueeful to remember what it's for!)
- The print statement when the noun is missing ("Unlock what?")
- pass the verb through to the puzzle trigger "UNLOCK"
- The failure message ("You can't unlock that.")

```python
DESCRIPTION = 'UNLOCK - unlock something (e.g. UNLOCK GRATE)'

def execute(player, noun):
    if noun is None:
        print('Unlock what?')
        return
    fired = player.game.puzzles.trigger(player, 'UNLOCK', noun, player.getRoom())
    if not fired:
        print("You can't unlock that.")

```

4. Set up the puzzle. When we unlock the grate with the keys, we need to add the exit from this room to the next, the exit back the other way, and change the state from 0 to 1. That's three rows — and we attach the "grate is now open" message directly to the final `SET_ITEM_STATE` row rather than needing a separate `PRINT_MSG` row first.

On all three:
- trigger_verb = UNLOCK
- trigger_item = GRATE
- trigger_room = 8 (in my example)
- condition_item = KEYS — you need this item in inventory for the puzzle to fire
- condition_item_state = grate:0 — you can only _open_ the grate if it's in state 0. If it's not in state 0, it's already open!
- once = FALSE — we only want it to fire once but we're dealing with that with the state change

Now the things that separate them:
- **Row 1** — ADD_EXIT effect type, effect_target = 8 (the current room), effect_value = _DOWN:9_ (it goes DOWN from 8 to 9)
- **Row 2** — ADD_EXIT effect type, effect_target = 9 (other room), effect_value = _UP:8_ (it goes UP from the other room to here)
- **Row 3** — SET_ITEM_STATE effect type, effect_target = grate, effect_value = 1 (change the grate to state 1 — it works by name so catches them all). Add `message_file = grate_unlocked` (or `message = "The grate is now open."`) to this row so the player sees the result.

_Then_... you have to repeat those three rows with trigger_room = 9, just in case they somehow reach room 9 first. And remember — order matters. If you change the state on the first row, none of the rest will fire!

__TEST__
This test code should turn on debug, get the keys, jump to the grate, try to get down (fail), unlock, go down, and try to unlock from the other side (fail due to already being unlocked).
```
DEBUG
CHEAT 3
GET KEYS
CHEAT 8
DOWN
UNLOCK GRATE
DOWN
UNLOCK GRATE
```

### Light and Dark
It is common to have some areas that are lit, and some that are not. A light source is needed to deal with the dark!

__Adventure example:__ There is a lamp in room 3 which you need to TAKE then ON to be able to see in the caves. It has 330 units of oil which decrement every turn when the lamp is on.

1. **Mark rooms as lit or dark.** In `rooms.csv`, each room has a `lit` column. Set it to `TRUE` for rooms with natural light (outdoors, rooms with windows, etc.) and `FALSE` for anywhere that needs a light source. Rooms default to `FALSE` if the column is blank. In Adventure, rooms 1–10 are naturally lit (above ground) and everything underground is dark.

2. **Set the dark message.** In `settings.csv`, the `dark_message` setting controls what the player sees when they enter a dark room without light. The Adventure default is _IT IS NOW PITCH DARK. IF YOU PROCEED YOU WILL LIKELY FALL INTO A PIT._ Change this to suit your game.

3. **Create the light item.** In `items.json`, a light source needs two extra fields beyond a normal item:
   - `room_desc` — use two entries for unlit and lit states, e.g. `["There is a brass lamp here.", "There is a glowing brass lamp here."]`
   - `light_turns` — how many turns of light it provides. Omit or set to `0` for non-light-sources. The Adventure lamp has `330`.

   The item otherwise works like any other — give it `id_words`, a `gettable` of `true`, and place it in a room.

4. **Create the ON and OFF commands.** Copy `commands/game/on.py` and `commands/game/off.py`. The `ON` command checks the player is carrying the item by name, sets its `state` to 1 (switching to the lit `room_desc`) and calls `setMakingLight(1)`. `OFF` reverses this. You can also add aliases — Adventure uses `LIGHT` for on and `EXTINGUISH`/`EXTIN` for off.

   The engine handles the rest automatically:
   - Each turn the lamp is lit, `turns_remaining` decrements by 1
   - When it hits 0, `making_light` is set to 0 and `state` drops back to 0 — the lamp goes out
   - `isLocationLit()` checks both the player's inventory and the current room, so a dropped lamp still lights the room it's left in

5. **Add warning messages.** Use FORCE puzzle rows with `condition_item_turns_eq` to warn the player before the lamp dies. Set `condition_item_state=lamp:1` so warnings only fire while the lamp is lit. For example:
   - `lamp:50` → "Your lamp is getting dim."
   - `lamp:30` → "Your lamp is running very low."
   - `lamp:1` → "Your lamp has run out of power." (fires on the last lit turn, just before the engine extinguishes it)

6. **Add dark room danger.** Without a light source, players should risk death after wandering in the dark. The Adventure original fires a 35% death chance per move after the player's first move in darkness. Set this up with three FORCE rows:
   - `condition_location_dark=true` → `INCREMENT_COUNTER dark_moves` — counts moves spent in the dark
   - `condition_location_dark=false` → `RESET_COUNTER dark_moves` — resets when light is found
   - `condition_counter_gte=dark_moves:2`, `chance_pct=35` → `LOSE` — 35% death chance from the second dark move onward (the first move is always safe)

__TEST__
This test code should turn on debug, pick up the lamp, go somewhere dark, check it's dark, turn the lamp on, check you can now see, drop the lamp and move away, then return to confirm the lamp still lights the room.
```
DEBUG
CHEAT 3
GET LAMP
CHEAT 25
ON
LOOK
DROP LAMP
UP
DOWN
```

### Getting an item only when you have another item

Sometimes an item can only be picked up if the player already has a specific item. You can also block the action if the player is carrying something that gets in the way.

__Adventure example:__ The bird in room 13 can only be caught if the player is carrying the wicker cage. If they are carrying the black rod (rod1), the bird is frightened and cannot be caught.

1. **Make the item non-gettable.** In `items.json`, set `"gettable": false` for the bird. This prevents the normal GET command from picking it up. Give it two `room_desc` entries — one for when it's free, one for when it's in the cage: `["A CHEERFUL LITTLE BIRD IS SITTING HERE SINGING.", "THERE IS A LITTLE BIRD IN THE CAGE."]`

2. **Add the GET puzzles.** The GET command fires puzzles before attempting a normal pick-up. If any puzzle fires, the normal pick-up is skipped entirely. Add three rows in `puzzles.csv`, all with `trigger_verb=GET`, `trigger_item=BIRD`, `trigger_room=13`:

   - **Row 1 — rod frightens the bird:** `condition_item=ROD1`. Effect: `PRINT_MSG` — "THE BIRD WAS UNAFRAID WHEN YOU ENTERED, BUT AS YOU APPROACH IT BECOMES DISTURBED AND YOU CANNOT CATCH IT." Set `once=FALSE` so it fires every time.
   - **Row 2 — no cage:** `condition_not_item=ROD1,CAGE` (player has neither). Effect: `PRINT_MSG` — "YOU CAN CATCH THE BIRD, BUT YOU CANNOT CARRY IT." Set `once=FALSE`.
   - **Row 3 — success (has cage, no rod):** `condition_item=CAGE`, `condition_not_item=ROD1`. Two effects on separate rows: `GIVE_ITEM` with target `bird` (moves bird from room to inventory), then `SET_ITEM_STATE` with target `bird` and value `1` (switches to the "in cage" description). Set `once=FALSE` — the puzzle engine handles repeat attempts naturally since the bird won't be in the room a second time.

   Order matters: put the rod-blocking row first so it takes priority over the success row when the player has both.

__TEST__
```
DEBUG
CHEAT 3
GET LAMP
GET KEYS
OUT
S
S
S
UNLOCK GRATE
D
W
GET CAGE
ON
W
GET ROD
W
W
GET BIRD
DROP ROD
GET BIRD
I
```

### Using one item to clear a creature blocking your path

Sometimes a creature blocks movement in a room. Another item (or a sacrifice) is needed to clear it and open up new exits.

__Adventure example:__ A snake blocks the south and west exits of the Hall of the Mountain King (room 19). Dropping the bird (which must be in the cage) in that room causes it to attack and drive the snake away, opening those exits. Both the bird and the snake are destroyed in the process.

1. **Add the creature as an item.** In `items.json`, set `"gettable": false` and give it a single `room_desc` entry — the message seen when the creature is present. There's no need for a second state since the creature will be completely removed from the game. Place it in the blocking room.

2. **Add the DROP puzzle.** When the player drops the sacrificial item in the right room (and the creature is still there), several things need to happen in sequence. Add rows in `puzzles.json` with `trigger_verb=DROP`, `trigger_item=BIRD`, `trigger_room=19`, and `condition_room_item=SNAKE` on every row (so it only fires while the snake is still there):

   - **Row 1 — destroy the sacrificial item:** `DESTROY_ITEM` with target `bird`. Add the flavour text as `message` on this row — it prints before the effect runs.
   - **Row 2 — destroy the creature:** `DESTROY_ITEM` with target `snake`.
   - **Rows 3-4 — open the exits:** `ADD_EXIT` for each direction that was blocked. Here `ADD_EXIT` on room 19 for `SOUTH:36` and `WEST:37`.

   Note: in Adventure these exits are one-way — you can go south/west from room 19 but there is no route back. That's intentional and valid.

3. **No command file needed.** The DROP command already triggers puzzles after a successful drop — nothing extra required.

__TEST__
```
DEBUG
CHEAT 3
GET LAMP
GET KEYS
OUT
S
S
S
UNLOCK GRATE
D
W
GET CAGE
ON
W
GET ROD
W
W
GET BIRD
DROP ROD
GET BIRD
W
D
N
DROP BIRD
```

### Blocking a direction with a custom message

Compass directions (`NORTH`, `SOUTH`, `EAST`, `WEST`, `NE`, `NW`, `SE`, `SW`, `UP`, `DOWN`) check puzzles before attempting movement. If any puzzle fires, the movement is cancelled. This lets you display a specific message when a passage is blocked — rather than the generic "I cannot move that way."

__Adventure example:__ The snake blocks the south and west exits of room 19. Trying to go south or west before clearing the snake prints "You can't get by the snake." instead of a generic failure.

1. **Leave the exits out of `rooms.csv`.** Don't add the blocked directions to the room's exit list — they'll be added later by the puzzle that clears the blocker (e.g. `ADD_EXIT`).

2. **Add the blocking puzzle rows.** In `puzzles.json`, add one row per blocked direction with `trigger_verb=SOUTH` (or whichever direction), `trigger_room=19`, `condition_room_item=SNAKE`, effect `PRINT_MSG`, and the message to display. Set `once=FALSE`.

   Because the puzzle fires and returns true, the movement command is cancelled — the player stays put.

3. **No command file changes needed.** All compass direction aliases already check puzzles first.

__TEST__
```
CHEAT 19
SOUTH
WEST
```

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
