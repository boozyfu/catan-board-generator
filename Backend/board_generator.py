import random
from PIL import Image
import math
import streamlit as st
#initialize
row_lengths = [3, 4, 5, 4, 3]

if "image_files" not in st.session_state:
  img_files = glob.glob("./Images/*.png")
  st.session_state.image_files = img_files

if "img_stem" not in st.session_state:
  st.session_state.img_stem = [f.split("/")[-1] for f in st.session_state.image_files]

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
    for row_len in row_lengths:
        board.append(tiles[i : i + row_len])
        i += row_len
    return board

@st.cache_data
def load_board_images(tile_size=40):
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

def display_board(resource_dict):
  board_image_lookup = load_board_images()
  st.write(board_image_lookup.keys())
  board = generate_board(resource_dict)
  
  tile_size = 40
  
  # Calculate canvas size
  # For hexagonal grids with offset rows
  max_width = max(len(row) for row in board)
  canvas_width = max_width * tile_size + tile_size // 2
  canvas_height = len(board) * tile_size + tile_size // 2
  
  # Create blank image
  board_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
  
  # Paste tiles
  for row_num, row in enumerate(board):
    for col_num, resource in enumerate(row):
      # Calculate x position with offset for alternating rows
      offset_x = (tile_size // 2) if row_num % 2 == 1 else 0
      x = col_num * tile_size + offset_x + (tile_size // 4)
      y = row_num * tile_size + (tile_size // 4)
      
      tile_img = board_image_lookup[resource]
      board_image.paste(tile_img, (int(x), int(y)), tile_img)
  
  st.image(board_image)
