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
    for row_len in ROW_LENGTHS:
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
            .rotate(30, expand=True)
        )
    return images

def create_composite_image(resource_dict, coordinates=CATAN_COORDS, canvas_size=(200, 100)):
    """Place images at specified coordinates on a canvas."""
    canvas = Image.new('RGB', canvas_size, color='white')
    board = generate_board(resource_dict)
    
    board_images = load_board_images()
    
    # Flatten the board and zip with coordinates
    flat_board = [tile for row in board for tile in row]
    
    for tile, (x, y) in zip(flat_board, coordinates):
        img = board_images.get(tile)
        if img:  # Check if image exists
            left = x - img.width // 2
            top = y - img.height // 2
            canvas.paste(img, (left, top), img)  # Use alpha channel for transparency
    
    return canvas
