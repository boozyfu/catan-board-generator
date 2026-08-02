import random
from board_generator import generate_numbers

def build_neighbors(rows):
    positions = []
    for r, length in enumerate(rows):
        for c in range(length):
            positions.append((r, c))

    index = {p: i for i, p in enumerate(positions)}
    neighbors = [[] for _ in positions]

    for r, c in positions:
        i = index[(r, c)]

        # Same row
        for nc in (c - 1, c + 1):
            if (r, nc) in index:
                neighbors[i].append(index[(r, nc)])

        # Row above
        if r > 0:
            if rows[r - 1] < rows[r]:
                candidates = [(r - 1, c - 1), (r - 1, c)]
            else:
                candidates = [(r - 1, c), (r - 1, c + 1)]

            for p in candidates:
                if p in index:
                    neighbors[i].append(index[p])

        # Row below
        if r < len(rows) - 1:
            if rows[r + 1] < rows[r]:
                candidates = [(r + 1, c - 1), (r + 1, c)]
            else:
                candidates = [(r + 1, c), (r + 1, c + 1)]

            for p in candidates:
                if p in index:
                    neighbors[i].append(index[p])

    return neighbors

def valid_numbers(numbers, neighbors):
    for i, value in enumerate(numbers):
        if value not in (6, 8):
            continue

        for j in neighbors[i]:
            if numbers[j] in (6, 8):
                return False

    return True



neighbors = build_neighbors([3,4,5,4,3])

num_list = generate_numbers(game_type)

hex_list = [img for row in image_board for img in row]

num_list = [
    None if img in ("desert", "water")
    else num_list.pop(0)
    for img in hex_list
 ]


neighbors = build_neighbors(row_lengths)

while True:
    numbers = generate_numbers(game_type)[:]  # copy
    random.shuffle(numbers)

    board_numbers = [
        None if img in ("desert", "water")
        else numbers.pop(0)
        for img in hex_list
    ]

    if valid_numbers(board_numbers, neighbors):
        break

num_list = board_numbers
