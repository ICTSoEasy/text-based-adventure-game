DESCRIPTION = "Show your current score (SCORE DETAILS for breakdown)"

def execute(player, noun):
    game = player.game
    details = noun and noun.upper() == 'DETAILS'
    default_deposit_room_id = game.settings.get('deposit_room', 3)

    # Collect all items including destroyed ones
    all_items = []
    for room in game.rooms.values():
        all_items.extend(room.getContains())
    all_items.extend(player.items)
    all_items.extend(game.destroyed_items)

    scoreable = [i for i in all_items if i.finding_bonus or i.deposit_bonus]

    score = 0
    for item in scoreable:
        if not item.found:
            continue
        score += item.finding_bonus
        dr_id = item.deposit_room if item.deposit_room else default_deposit_room_id
        dr = game.rooms.get(dr_id)
        in_deposit_room = dr and item in dr.getContains()
        if in_deposit_room:
            score += item.deposit_bonus
        if details:
            line = f'{item.getShortDesc().capitalize()} found ({item.finding_bonus})'
            if in_deposit_room and item.deposit_bonus:
                room_name = dr.getShortDesc().lower() if dr else f'room {dr_id}'
                line += f' and deposited in {room_name} ({item.deposit_bonus})'
            print(line)

    max_score = sum(i.finding_bonus + i.deposit_bonus for i in scoreable)
    print(f'If you were to quit now, you would score {score} out of a possible {max_score}.')
