# Implementation Notes — CCA-350

Reference for continuing work. Data files are in `advent_data/originals/`.

---

## Original game item numbering

Items in `5 - object descriptions.txt` and `7 - object locations.txt` use the **original** numbering (1–64). Our `items.json` uses **different IDs** for some items — notably:

| Our ID | Original ID | Item |
|--------|-------------|------|
| 17 | 57 | Jeweled trident |
| 16 | 16 | Spelunker Today |
| 58 | 58 | Ming vase |
| 61 | 61 | Glistening pearl |

### 1000-series convention (two-location items)

Items that exist in two rooms simultaneously have a second entry with ID = original_id + 1000. The original game stores both locations in the FIXD/PLAC arrays; we create two Thing objects instead.

Items that need this (original IDs with two locations in `7 - object locations.txt`):
- 3 → grate in rooms 8 and 9 (done: items 3 and 1003)
- 7 → steps in rooms 14 and 15 (done: items 7 and 1007)
- 12 → fissure in rooms 17 and 27 (done: items 12 and 1012)
- 25 → phony plant in rooms 23 and 67 (not yet implemented)
- 31 → dragon in rooms 119 and 121 (not yet implemented)
- 32 → chasm in rooms 117 and 122 (not yet implemented)
- 33 → troll in rooms 117 and 122 (not yet implemented)
- 62 → Persian rug in rooms 119 and 121 (not yet implemented)

### Items 17 and 18 — DWARF and KNIFE

Items 17 and 18 have **no entries in the object descriptions file** because they are not normal items. In the vocabulary file (`4 - vocabulary.txt`):
- `1017` = DWARF (object noun 17)
- `1018` = KNIFE (object noun 18)

The knife does not exist as a placed object — its location is tracked via the `KNFLOC` variable in the Fortran source. The dwarf system is a major separate subsystem (see below).

---

## Dwarf system (not yet implemented)

The original game has up to 6 dwarves, activated when the player first enters the Hall of Mists (room 18 area). Key behaviour from `advent.for`:

- `DLOC(6)` — current location of each dwarf
- `DFLAG` — activation level (0=not active, 1=reached mists, 2=met first dwarf, 3+=knives throwing)
- `DALTLC=18` — alternate starting location if a dwarf spawns on top of the player
- `DSEEN(6)` — whether each dwarf has seen the player
- `KNFLOC` — room where a thrown knife currently is (0=none, -1=player was warned)
- The 6th dwarf is the **pirate** — he starts near his chest's eventual hiding spot and steals treasures

Pirate behaviour: if the player carries a treasure and the pirate hasn't yet hidden his chest, the pirate steals everything and drops the chest in the maze (room 114 in the original).

This is a substantial system to implement and is not on the immediate roadmap.

---

## Open GitHub issues (as of 2026-04-12)

| # | Title | Notes |
|---|-------|-------|
| 1 | YES/NO prompt before play begins | Enhancement |
| 2 | DROP shows item ID instead of description | Bug |
| 3 | DROP struggles when holding both rods | Bug |
| 4 | LOOK at item repeats room description | Research |
| 5 | Getting item only when you have another (CREATOR.md review) | Review AI-generated docs |
| 6 | Using one item to clear a creature (CREATOR.md review) | Review AI-generated docs |
| 7 | Blocking a direction with a custom message (CREATOR.md review) | Review AI-generated docs |
| 8 | POINTS system | Research |
| 9 | Soft room | Research |
| 10 | Lamp dim/out messages via messages.csv (blocked on vending machine) | Bug |
| 11 | TALLY/TALLY2 | Enhancement |
| 12 | Puzzles don't catch MOVE NORTH / MOVE N | Bug |

---

## Items not yet in items.json (original game items we haven't added)

From `5 - object descriptions.txt`, items present in the original but not in our game:
- 19 — Tasty food (room 3)
- 21/22 — Water/oil in bottle (internal bottle states — bottle item 20 is done)
- 23 — Mirror (room 109, fixed)
- 24/25 — Plant / phony plant (rooms 25/23+67, fixed, multi-state)
- 26 — Stalactite (room 111, fixed)
- 27 — Shadowy figure (rooms 35+110)
- 28 — Dwarf's axe (room 0, unborn)
- 29 — Cave drawings (room 97, fixed)
- 30 — Pirate (room 0)
- 31 — Dragon (rooms 119+121, fixed)
- 32 — Chasm (rooms 117+122, fixed)
- 33 — Troll (rooms 117+122, fixed)
- 34 — Phony troll (room 0)
- 35 — Bear (room 130, fixed)
- 36 — Message in second maze (room 0)
- 37 — Volcano/geyser (room 126, fixed)
- 38 — Vending machine (room 140, fixed)
- 39 — Batteries (room 0, unborn)
- 40 — Carpet/moss (rooms 96+-1, fixed)
- 50 — Large gold nugget (room 18)
- 51 — Several diamonds (room 27)
- 52 — Bars of silver (room 28)
- 53 — Precious jewelry (room 29)
- 54 — Rare coins (room 30)
- 55 — Treasure chest (room 0, unborn — pirate hides it)
- 56 — Golden eggs (room 92)
- 59 — Egg-sized emerald (room 100)
- 60 — Platinum pyramid (room 101)
- 62 — Persian rug (rooms 119+121)
- 63 — Rare spices (room 127)
- 64 — Golden chain (room 130, fixed)

---

## Key source files

| File | Contents |
|------|----------|
| `advent_data/originals/advent.for` | Full Fortran source — game logic, dwarf system, scoring |
| `advent_data/originals/1 - long room descriptions.txt` | Full room text |
| `advent_data/originals/2 - short room descriptions.txt` | Short room names |
| `advent_data/originals/3 - travel table (exits).txt` | All exits/conditions |
| `advent_data/originals/4 - vocabulary.txt` | All words (1xxx=nouns, 2xxx=verbs) |
| `advent_data/originals/5 - object descriptions.txt` | Item names and room_desc strings |
| `advent_data/originals/6 - game messages.txt` | All game messages (numbered) |
| `advent_data/originals/7 - object locations.txt` | Starting room(s) for each item |
| `advent_data/originals/8 - action defaults.txt` | Default verb responses |
| `advent_data/originals/9 - conditions.txt` | Room condition flags |
