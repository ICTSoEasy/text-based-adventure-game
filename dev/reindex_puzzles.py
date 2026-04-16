#!/usr/bin/env python3
"""Re-index puzzle IDs in puzzles.json sequentially, preserving all formatting."""
import re
import sys

input_file = 'puzzles.json'
output_file = 'puzzles.json'

with open(input_file, 'r') as f:
    lines = f.readlines()

counter = 1
new_lines = []
for line in lines:
    # Only rewrite lines that have an "id" field and are not comment-only lines
    if re.search(r'"id"\s*:', line) and '"_comment"' not in line:
        line = re.sub(r'("id"\s*:\s*)\d+', lambda m: m.group(1) + str(counter), line)
        counter += 1
    new_lines.append(line)

with open(output_file, 'w') as f:
    f.writelines(new_lines)

print(f'Done. {counter - 1} puzzles re-indexed.')
