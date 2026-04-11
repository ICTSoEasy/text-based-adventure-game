import csv
import time
import random

class PuzzleEngine:
    def __init__(self, game):
        self.game = game
        self.puzzles = []
        self.fired = set()  # tracks group keys for once=True puzzles

    def load(self, filename='puzzles.csv'):
        debug = self.game.settings.get('debug', False)
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                first = list(row.values())[0].strip()
                if first.startswith(';'):
                    if debug:
                        print(f'  [comment] {first[1:].strip()}')
                else:
                    self.puzzles.append(row)

    def trigger(self, player, verb, item_name, room_id):
        """Check all puzzles for a matching trigger and apply effects. Returns True if anything fired."""
        fired_any = False
        keys_fired_this_call = set()
        debug = self.game.settings.get('debug', False)

        for puzzle in self.puzzles:
            if not self._matches(puzzle, player, verb, item_name, room_id):
                continue

            key = (
                puzzle['trigger_verb'].strip().upper(),
                puzzle['trigger_item'].strip().upper(),
                puzzle['trigger_room'].strip(),
                puzzle.get('condition_item_turns_eq', '').strip()
            )

            # Skip once-only puzzles that have already fired
            if puzzle['once'].strip().lower() == 'true' and key in self.fired:
                continue

            if debug:
                tv = puzzle['trigger_verb'].strip()
                ti = puzzle['trigger_item'].strip()
                tr = puzzle['trigger_room'].strip()
                ef = puzzle['effect_type'].strip()
                print(f'  [puzzle] {tv} {ti} room={tr} → {ef}')

            self._apply(player, puzzle)
            fired_any = True

            if puzzle['once'].strip().lower() == 'true':
                keys_fired_this_call.add(key)

        # Mark once-only groups as fired after processing all rows
        self.fired.update(keys_fired_this_call)
        return fired_any

    def _matches(self, puzzle, player, verb, item_name, room_id):
        item_name = (item_name or '').upper()

        # Verb must match
        if puzzle['trigger_verb'].strip().upper() != verb.upper():
            return False

        # trigger_item: if specified, must match
        ti = puzzle['trigger_item'].strip().upper()
        if ti and ti != item_name:
            return False

        # trigger_room: if specified, must match
        tr = puzzle['trigger_room'].strip()
        if tr and int(tr) != room_id:
            return False

        # condition_item: player must be carrying this
        ci = puzzle['condition_item'].strip().upper()
        if ci and not player.hasItem(ci):
            return False

        # condition_not_item: player must NOT be carrying any of these (comma-separated)
        cni = puzzle['condition_not_item'].strip().upper()
        if cni:
            for item_name in [x.strip() for x in cni.split(',')]:
                if item_name and player.hasItem(item_name):
                    return False

        # condition_room_item: this item must be in the current room
        cri = puzzle['condition_room_item'].strip().upper()
        if cri:
            room = self.game.getRoom(room_id)
            if not room.ifContains(cri):
                return False

        # condition_item_state: item_name:state — named item must be in that state
        cis = puzzle.get('condition_item_state', '').strip()
        if cis:
            cis_name, cis_state = cis.split(':')
            items = self.game.findAllItems(cis_name.upper())
            if not items or items[0].state != int(cis_state):
                return False

        # condition_item_turns_eq: item_name:value — named item's turns_remaining must equal value
        cite = puzzle.get('condition_item_turns_eq', '').strip()
        if cite:
            cite_name, cite_value = cite.split(':')
            items = self.game.findAllItems(cite_name.upper())
            if not items or items[0].getTurnsRemaining() != int(cite_value):
                return False

        # condition_location_dark: true/false — whether the player's location is dark
        cld = puzzle.get('condition_location_dark', '').strip().lower()
        if cld == 'true' and player.isLocationLit():
            return False
        if cld == 'false' and not player.isLocationLit():
            return False

        # condition_counter_gte: counter_name:value — named counter must be >= value
        ccg = puzzle.get('condition_counter_gte', '').strip()
        if ccg:
            ccg_name, ccg_value = ccg.split(':')
            if self.game.counters.get(ccg_name, 0) < int(ccg_value):
                return False

        # chance_pct: integer 1-100 — percentage chance this row fires at all
        pct = puzzle.get('chance_pct', '').strip()
        if pct and not random.randint(1, 100) <= int(pct):
            return False

        return True

    def _apply(self, player, puzzle):
        effect = puzzle['effect_type'].strip().upper()
        target = puzzle['effect_target'].strip()
        value = puzzle['effect_value'].strip()
        message = puzzle['message'].strip()
        delay_str = puzzle['delay'].strip()
        delay = float(delay_str) if delay_str else 0

        if message:
            print(message)
        if delay:
            time.sleep(delay)

        if effect == 'PRINT_MSG':
            pass  # message already printed above

        elif effect == 'ADD_EXIT':
            direction, dest_room = value.split(':')
            self.game.getRoom(int(target)).addExit(direction.strip(), int(dest_room.strip()))

        elif effect == 'REMOVE_EXIT':
            self.game.getRoom(int(target)).removeExit(value)

        elif effect == 'SET_ROOM_LONG_DESC':
            self.game.getRoom(int(target)).setLongDesc(value)

        elif effect == 'SHOW_ROOM_LONG_DESC':
            room_id = int(target) if target else player.getRoom()
            print(self.game.getRoom(room_id).getLongDesc())

        elif effect == 'SET_ITEM_SHORT_DESC':
            item = self.game.findItem(target.upper())
            if item:
                item.setShortDesc(value)

        elif effect == 'TELEPORT':
            player.setRoom(int(value))
            player.look()

        elif effect == 'SET_ITEM_STATE':
            for item in self.game.findAllItems(target.upper()):
                item.setState(int(value))

        elif effect == 'SET_ITEM_LONG_DESC':
            item = self.game.findItem(target.upper())
            if item:
                item.setLongDesc(value)

        elif effect == 'SHOW_MESSAGE':
            msg = self.game.messages.get(target)
            if msg:
                print(msg)
            else:
                print(f'[Message not found: {target}]')

        elif effect == 'GIVE_ITEM':
            room = self.game.getRoom(player.getRoom())
            item = room.ifContains(target.upper())
            if item:
                room.remove(item)
                player.items.append(item)

        elif effect == 'INCREMENT_COUNTER':
            self.game.counters[target] = self.game.counters.get(target, 0) + 1
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = {self.game.counters[target]}')

        elif effect == 'RESET_COUNTER':
            self.game.counters[target] = 0
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = 0 (reset)')

        elif effect == 'WIN':
            player.game.flipPlayStatus()

        elif effect == 'LOSE':
            player.kill()

        else:
            print(f'[Unknown effect type: {effect}]')
