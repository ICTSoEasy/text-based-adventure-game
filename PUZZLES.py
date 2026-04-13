import json
import time
import random

class PuzzleEngine:
    def __init__(self, game):
        self.game = game
        self.puzzles = []
        self.fired = set()  # tracks group keys for once=True puzzles

    def load(self, filename='puzzles.json'):
        debug = self.game.settings.get('debug', False)
        with open(filename, encoding='utf-8') as f:
            rows = json.load(f)
        for row in rows:
            if '_comment' in row and len(row) == 1:
                if debug:
                    print(f'  [comment] {row["_comment"]}')
            else:
                self.puzzles.append(row)

    def _f(self, puzzle, key):
        """Get field value as a stripped string, defaulting to ''."""
        val = puzzle.get(key)
        return '' if val is None else str(val).strip()

    def has_verb(self, verb):
        """Return True if any puzzle row uses this verb."""
        return any(verb.upper() in [v.strip() for v in self._f(p, 'trigger_verb').upper().split(',')] for p in self.puzzles)

    def trigger(self, player, verb, item_name, room_id):
        """Check all puzzles for a matching trigger and apply effects. Returns True if anything fired."""
        fired_any = False
        keys_fired_this_call = set()
        debug = self.game.settings.get('debug', False)

        for puzzle in self.puzzles:
            if not self._matches(puzzle, player, verb, item_name, room_id):
                continue

            key = (
                self._f(puzzle, 'trigger_verb').upper(),
                self._f(puzzle, 'trigger_item').upper(),
                self._f(puzzle, 'trigger_room'),
                self._f(puzzle, 'condition_item_turns_eq')
            )

            # Skip once-only puzzles that have already fired
            once = puzzle.get('once', False)
            if (once is True or str(once).lower() == 'true') and key in self.fired:
                continue

            if debug:
                pid = puzzle.get('id', '?')
                tv = self._f(puzzle, 'trigger_verb')
                ti = self._f(puzzle, 'trigger_item')
                tr = self._f(puzzle, 'trigger_room')
                ef = self._f(puzzle, 'effect_type')
                print(f'  [puzzle #{pid}] {tv} {ti} room={tr} → {ef}')

            self._apply(player, puzzle, item_name)
            fired_any = True

            if once is True or str(once).lower() == 'true':
                keys_fired_this_call.add(key)

            stop = puzzle.get('stop', False)
            if stop is True or str(stop).lower() == 'true':
                break

        # Mark once-only groups as fired after processing all rows
        self.fired.update(keys_fired_this_call)
        return fired_any

    def _matches(self, puzzle, player, verb, item_name, room_id):
        item_name = (item_name or '').upper()

        # Verb must match (comma-separated list allowed)
        tv = self._f(puzzle, 'trigger_verb').upper()
        if verb.upper() not in [v.strip() for v in tv.split(',')]:
            return False

        # trigger_item: comma-separated list of accepted noun patterns.
        # Each entry can be:
        #   BOTTLE        → typed word must be BOTTLE, existence checked for BOTTLE
        #   OIL>BOTTLE    → typed word must be OIL, existence checked for BOTTLE
        #   >BOTTLE       → typed word must be absent (bare verb), existence checked for BOTTLE
        ti_raw = self._f(puzzle, 'trigger_item').upper()
        if ti_raw:
            item_name_up = (item_name or '').upper()
            room = self.game.getRoom(room_id)
            matched = False
            for entry in [e.strip() for e in ti_raw.split(',')]:
                if '>' in entry:
                    ti_match, ti_check = entry.split('>', 1)
                else:
                    ti_match = ti_check = entry
                # Check typed word matches
                if ti_match == '' and item_name_up != '':
                    continue  # empty left = bare verb only
                if ti_match != '' and ti_match != item_name_up:
                    continue
                # Check item exists in room or inventory
                in_room = room.ifContains(ti_check) if room and ti_check else None
                in_inv = player.hasItem(ti_check) if ti_check else None
                if ti_check and not in_room and not in_inv:
                    continue
                matched = True
                break
            if not matched:
                return False

        # trigger_room: if specified, must match
        tr = self._f(puzzle, 'trigger_room')
        if tr and int(tr) != room_id:
            return False

        # condition_item: player must be carrying this
        ci = self._f(puzzle, 'condition_item').upper()
        if ci and not player.hasItem(ci):
            return False

        # condition_not_item: player must NOT be carrying any of these (comma-separated)
        cni = self._f(puzzle, 'condition_not_item').upper()
        if cni:
            for ni in [x.strip() for x in cni.split(',')]:
                if ni and player.hasItem(ni):
                    return False

        # condition_room_item: all listed items must be in the current room
        cri = self._f(puzzle, 'condition_room_item').upper()
        if cri:
            room = self.game.getRoom(room_id)
            for ri in [x.strip() for x in cri.split(',')]:
                if ri and not room.ifContains(ri):
                    return False

        # condition_not_room_item: this item must NOT be in the current room (comma-separated)
        cnri = self._f(puzzle, 'condition_not_room_item').upper()
        if cnri:
            room = self.game.getRoom(room_id)
            for ni in [x.strip() for x in cnri.split(',')]:
                if ni and room.ifContains(ni):
                    return False

        # condition_companion: all listed items must be current companions (comma-separated)
        cc = self._f(puzzle, 'condition_companion').upper()
        if cc:
            for name in [x.strip() for x in cc.split(',')]:
                if name and not any(c.matchesName(name) for c in player.companions):
                    return False

        # condition_not_companion: none of these may be current companions (comma-separated)
        cnc = self._f(puzzle, 'condition_not_companion').upper()
        if cnc:
            for name in [x.strip() for x in cnc.split(',')]:
                if name and any(c.matchesName(name) for c in player.companions):
                    return False

        # condition_item_state: item_name:state — named item must be in that state (comma-separated for multiple)
        cis = self._f(puzzle, 'condition_item_state')
        if cis:
            for pair in [p.strip() for p in cis.split(',')]:
                cis_name, cis_state = pair.split(':')
                items = self.game.findAllItems(cis_name.upper())
                if not items or items[0].state != int(cis_state):
                    return False

        # condition_trigger_item_min_deposit: trigger item must have deposit_bonus >= this value
        ctd = self._f(puzzle, 'condition_trigger_item_min_deposit')
        if ctd:
            trigger_item = self.game.findItem(item_name) if item_name else None
            if not trigger_item or trigger_item.deposit_bonus < int(ctd):
                return False

        # condition_item_turns_eq: item_name:value — named item's turns_remaining must equal value
        cite = self._f(puzzle, 'condition_item_turns_eq')
        if cite:
            cite_name, cite_value = cite.split(':')
            items = self.game.findAllItems(cite_name.upper())
            if not items or items[0].getTurnsRemaining() != int(cite_value):
                return False

        # condition_location_dark: true/false — whether the player's location is dark
        cld = self._f(puzzle, 'condition_location_dark').lower()
        if cld == 'true' and player.isLocationLit():
            return False
        if cld == 'false' and not player.isLocationLit():
            return False

        # condition_counter_gte: counter_name:value — named counter must be >= value
        ccg = self._f(puzzle, 'condition_counter_gte')
        if ccg:
            ccg_name, ccg_value = ccg.split(':')
            if self.game.counters.get(ccg_name, 0) < int(ccg_value):
                return False

        # condition_counter_is: counter_name:value — named counter must equal value exactly
        cci = self._f(puzzle, 'condition_counter_is')
        if cci:
            cci_name, cci_value = cci.split(':')
            if self.game.counters.get(cci_name, 0) != int(cci_value):
                return False

        # condition_counter_exists: counter_name — counter must have been set (exists at all)
        cce = self._f(puzzle, 'condition_counter_exists')
        if cce:
            if cce not in self.game.counters:
                return False

        # condition_counter_not: counter_name:value — named counter must NOT equal value
        ccn = self._f(puzzle, 'condition_counter_not')
        if ccn:
            ccn_name, ccn_value = ccn.split(':')
            if self.game.counters.get(ccn_name, 0) == int(ccn_value):
                return False

        # chance_pct: integer 1-100 — percentage chance this row fires at all
        pct = self._f(puzzle, 'chance_pct')
        if pct and not random.randint(1, 100) <= int(pct):
            return False

        return True

    def _apply(self, player, puzzle, item_name=None):
        effect = self._f(puzzle, 'effect_type').upper()
        target = self._f(puzzle, 'effect_target')
        if target and target.upper() == 'TRIGGER_ITEM':
            target = item_name or ''
        value = self._f(puzzle, 'effect_value')
        message = self._f(puzzle, 'message')
        delay_raw = puzzle.get('delay') or 0
        delay = float(delay_raw)

        if not message:
            message = self.game.messages.get(self._f(puzzle,'message_file'))
        if message:
            print(message)
        if delay:
            time.sleep(delay)

        if effect == 'PRINT_MSG':
            pass  # message already printed above

        elif effect == 'ADD_EXIT':
            for pair in value.split(','):
                direction, dest_room = pair.split(':')
                self.game.getRoom(int(target)).addExit(direction.strip(), int(dest_room.strip()))

        elif effect == 'REMOVE_EXIT':
            for direction in value.split(','):
                self.game.getRoom(int(target)).removeExit(direction.strip())

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
            player._move_companions()
            player.look()

        elif effect == 'SET_ITEM_STATE':
            for item in self.game.findAllItems(target.upper()):
                item.setState(int(value))

        elif effect == 'SET_ITEM_LONG_DESC':
            item = self.game.findItem(target.upper())
            if item:
                item.setLongDesc(value)

        elif effect == 'PRINT_MSG_FILE':
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

        elif effect == 'DESTROY_ITEM':
            for item in self.game.findAllItems(target.upper()):
                for room in self.game.rooms.values():
                    if item in room.getContains():
                        room.remove(item)
                for inv_item in list(player.items):
                    if inv_item is item:
                        player.items.remove(inv_item)
                if item in player.companions:
                    player.companions.remove(item)
                self.game.destroyed_items.append(item)

        elif effect == 'HIDE_ITEM':
            for item in self.game.findAllItems(target.upper()):
                for room in self.game.rooms.values():
                    if item in room.getContains():
                        room.remove(item)
                        break
                if item in player.items:
                    player.items.remove(item)
                if item in player.companions:
                    player.companions.remove(item)
                if item not in self.game.hidden_items:
                    self.game.hidden_items.append(item)

        elif effect == 'SHOW_ITEM':
            dest_id = int(value) if value else player.getRoom()
            name = target.upper()
            placed = False
            for item in list(self.game.hidden_items):
                if item.matchesName(name):
                    self.game.hidden_items.remove(item)
                    self.game.getRoom(dest_id).putIn(item)
                    placed = True
                    break
            if not placed:
                for item in list(self.game.unborn_items):
                    if item.matchesName(name):
                        self.game.unborn_items.remove(item)
                        self.game.getRoom(dest_id).putIn(item)
                        break

        elif effect == 'ADD_COMPANION':
            item = self.game.findItem(target.upper())
            if item:
                for room in self.game.rooms.values():
                    if item in room.getContains():
                        room.remove(item)
                        break
                self.game.getRoom(player.getRoom()).putIn(item)
                if item not in player.companions:
                    player.companions.append(item)

        elif effect == 'CREATE_ITEM':
            name = target.upper()
            dest_id = int(value) if value else player.getRoom()
            for item in list(self.game.unborn_items):
                if item.matchesName(name):
                    self.game.unborn_items.remove(item)
                    self.game.getRoom(dest_id).putIn(item)
                    break

        elif effect == 'RESET_COUNTER':
            self.game.counters[target] = 0
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = 0 (reset)')

        elif effect == 'START_COUNTER':
            self.game.counters[target] = int(value) if value else 0
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = {self.game.counters[target]} (started)')

        elif effect == 'INC_COUNTER':
            amount = int(value) if value else 1
            self.game.counters[target] = self.game.counters.get(target, 0) + amount
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = {self.game.counters[target]} (+{amount})')

        elif effect == 'DEC_COUNTER':
            amount = int(value) if value else 1
            self.game.counters[target] = self.game.counters.get(target, 0) - amount
            if self.game.settings.get('debug', False):
                print(f'  [counter] {target} = {self.game.counters[target]} (-{amount})')

        elif effect == 'SET_GETTABLE':
            for item in self.game.findAllItems(target.upper()):
                item.gettable = (value.upper() == 'TRUE')

        elif effect == 'DROP_ITEM':
            item = player.hasItem(target.upper())
            if item:
                player.items.remove(item)
                self.game.getRoom(player.getRoom()).putIn(item)

        elif effect == 'ADD_POINTS':
            self.game.score += int(value)

        elif effect == 'REMOVE_POINTS':
            self.game.score -= int(value)

        elif effect == 'WIN':
            player.game.flipPlayStatus()

        elif effect == 'LOSE':
            player.kill()

        else:
            debug = self.game.settings.get('debug', False)
            if debug:
                print(f'[Unknown effect type: {effect}]')
