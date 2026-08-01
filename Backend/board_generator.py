import random
from PIL import Image
import math
import streamlit as st
#initialize
row_lengths = [3, 4, 5, 4, 3]

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

CATAN_COORDS = [
    (-4,  2), (-4,  0), (-4, -2),
    (-2,  3), (-2,  1), (-2, -1), (-2, -3),
    ( 0,  4), ( 0,  2), ( 0,  0), ( 0, -2), ( 0, -4),
    ( 2,  3), ( 2,  1), ( 2, -1), ( 2, -3),
    ( 4,  2), ( 4,  0), ( 4, -2),
]

def generate_board(resource_dict):
    tiles = []
    for resource, count in resource_dict.items():
        tiles.extend([resource] * count)
    random.shuffle(tiles)

    board = []
    i = 0
    for row_len in row_lengths:
        board.append(tiles[i : i + row_len])
        i += row_len
    return board

@st.cache_data
def load_board_images(tile_size=120):
    images = {}
    # Convert list to tuple for hashability
    image_files = tuple(st.session_state.get("image_files", []))
    
    for file in image_files:
        name = file.split("/")[-1].replace(".png", "")
        images[name] = (
            Image.open(file)
            .convert("RGBA")
            .resize((tile_size, tile_size))
            .rotate(30, expand=False)
        )
    return images

def display_grid(board, images):
    max_cols = max(row_lengths)

    for row, row_len in zip(board, row_lenghts):
        # calculate padding needed on each side
        padding = (max_cols - row_len) // 2

        # create full row with empty spaces
        cols = st.columns([1] * max_cols)

        start = padding
        end = padding + row_len

        for i, resource in enumerate(row):
            with cols[start + i]:
                st.image(
                    images[resource],
                    use_container_width=True
                )
