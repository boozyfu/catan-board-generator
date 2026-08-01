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
    st.write(board)
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

if "board_images" not in st.session_state:
  st.session_state.board_images = load_board_images()

def display_board(resource_dict):
  board_image_lookup = load_board_images()
  board = generate_board(resource_dict)
  image_idx = 0
  for row_num, num_cols in enumerate(row_lengths):
      cols = st.columns(num_cols)
      for col in cols:
          with col:
            for img in board[image_idx]:
              st.image(board_image_lookup[img], use_container_width=True)
          image_idx += 1
