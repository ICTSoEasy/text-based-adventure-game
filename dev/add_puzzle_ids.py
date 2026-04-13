"""One-shot script to add id fields to every puzzle row in puzzles.json.
Puzzle rows start at 1000; movement commands (after the MOVEMENT COMMANDS
comment) start at 5000. _comment entries are skipped.
"""
import json

with open('puzzles.json', encoding='utf-8') as f:
    puzzles = json.load(f)

puzzle_counter = 1000
move_counter = 5000
in_movement_section = False

result = []
for row in puzzles:
    if '_comment' in row:
        if 'MOVEMENT COMMANDS' in row['_comment']:
            in_movement_section = True
        result.append(row)
        continue

    if in_movement_section:
        new_id = move_counter
        move_counter += 1
    else:
        new_id = puzzle_counter
        puzzle_counter += 1

    # Build new dict with id first
    new_row = {'id': new_id}
    new_row.update(row)
    result.append(new_row)

with open('puzzles.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f'Done. Puzzle IDs: 1000–{puzzle_counter - 1}, Movement IDs: 5000–{move_counter - 1}')
