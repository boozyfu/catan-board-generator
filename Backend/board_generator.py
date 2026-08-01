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

def create_composite_image(image_list, coordinates, canvas_size=(800, 600)):
    """
    Place images at specified coordinates on a canvas.
    coordinates: list of (x, y) tuples representing center positions
    """
    # Create blank canvas
    canvas = Image.new('RGB', canvas_size, color='white')
    
    for img, (x, y) in zip(image_list, coordinates):
        
        # Calculate top-left position (center the image at x, y)
        left = x - img.width // 2
        top = y - img.height // 2
        
        # Paste image on canvas
        canvas.paste(img, (left, top))
    
    return canvas
