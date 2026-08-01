import random
from PIL import Image
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

def render_board(board, images, TILE_SIZE=120):
    hex_w = TILE_SIZE
    hex_h = int(TILE_SIZE * 0.8)
    max_row_len = max(ROW_LENGTHS)

    canvas_w = int(hex_w * 0.75 * max_row_len + hex_w * 0.5)
    canvas_h = int(hex_h * len(ROW_LENGTHS) + hex_h)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

    for row_idx, row in enumerate(board):
        row_offset = (max_row_len - len(row)) * (hex_w * 0.375)
        y = int(row_idx * hex_h * 0.85)
        for col_idx, resource in enumerate(row):
            x = int(row_offset + col_idx * hex_w * 0.75)
            canvas.paste(images[resource], (x, y), images[resource])

    return canvas
