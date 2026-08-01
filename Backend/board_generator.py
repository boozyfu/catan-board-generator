import random
from PIL import Image
import math

#initialize board
ROW_LENGTHS = [3, 4, 5, 4, 3]

fp_resources = {
  "wood": 4,
  "clay": 3,
  "wool": 4,
  "grain": 4,
  "ore": 3,
  "desert": 1}

tp_resources = {
  "wood": 3,
  "clay": 2,
  "wool": 3,
  "grain": 3,
  "ore": 2,
  "desert": 1}

def generate_board(resource_dict):
    tiles = []
    for resource, count in resource_dict.items():
        tiles.extend([resource] * count)
    random.shuffle(tiles)

    board = []
    i = 0
    for row_len in ROW_LENGTHS:
        board.append(tiles[i : i + row_len])
        i += row_len
    return board

def render_board(board, images, tile_size=120):
    radius = tile_size / 2

    # Pointy-top hex spacing
    dx = math.sqrt(3) * radius
    dy = 1.5 * radius

    row_lengths = [len(row) for row in board]
    max_row_len = max(row_lengths)

    margin = tile_size

    canvas_w = int(max_row_len * dx + 2 * margin)
    canvas_h = int((len(board) - 1) * dy + 2 * margin + tile_size)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

    for row_idx, row in enumerate(board):
        row_offset = (max_row_len - len(row)) * dx / 2

        for col_idx, resource in enumerate(row):
            if resource not in images:
                continue

            img = images[resource]

            cx = margin + row_offset + col_idx * dx
            cy = margin + row_idx * dy

            canvas.paste(
                img,
                (
                    int(cx - img.width / 2),
                    int(cy - img.height / 2),
                ),
                img,
            )

    return canvas
