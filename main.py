import streamlit as st
import random
import glob
from PIL import Image
from Backend.board_generator import fp_resources, tp_resources, load_board_images, display_grid 

tile_size = 120
fp, tp, exp, help = st.tabs(["4-Person", "2-Person", "Expansion", "Help"])

if "image_files" not in st.session_state:
  img_files = glob.glob("./Images/*.png")
  st.session_state.image_files = img_files

if "img_stem" not in st.session_state:
  st.session_state.img_stem = [f.split("/")[-1] for f in st.session_state.image_files]

if "board_images" not in st.session_state:
  st.session_state.board_images = load_board_images()

st.write(st.session_state.board_images.keys())

images = load_board_images()
with fp:
  st.header("Catan Board Generator - 4 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      board = generate_board(resource_dict)
      display_grid(board, images)
