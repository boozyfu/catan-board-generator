import random
from PIL import Image
import math
import streamlit as st
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

CATAN_COORDS = [
    (-4,  2), (-4,  0), (-4, -2),
    (-2,  3), (-2,  1), (-2, -1), (-2, -3),
    ( 0,  4), ( 0,  2), ( 0,  0), ( 0, -2), ( 0, -4),
    ( 2,  3), ( 2,  1), ( 2, -1), ( 2, -3),
    ( 4,  2), ( 4,  0), ( 4, -2),
]

@st.cache_data
def load_board_images(tile_size=120):
    images = {}

    for file in st.session_state["image_files"]:
        name = file.split("/")[-1].replace(".png", "")

        images[name] = (
            Image.open(file)
            .convert("RGBA")
            .resize((tile_size, tile_size))
            .rotate(30, expand=True)
        )

    return images

def render_board(board, images, tile_size=120):
    radius = tile_size / 2

    dx = math.sqrt(3) * radius
    dy = 1.5 * radius

    max_cols = max(len(r) for r in board)

    margin = tile_size

    canvas_w = int(max_cols * dx + margin * 2)
    canvas_h = int(len(board) * dy + margin * 2)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

    X_OFFSET = 6
Y_OFFSET = 6

for r, row in enumerate(board):
    offset = (max_cols - len(row)) * dx / 2

    for c, resource in enumerate(row):
        img = images[resource]

        x = int(margin + offset + c * dx - tile_size / 2 + X_OFFSET)
        y = int(margin + r * dy - tile_size / 2 + Y_OFFSET)

        canvas.alpha_composite(img, (x, y))


    return canvas
