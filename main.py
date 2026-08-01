import streamlit as st
import random
import glob
from PIL import Image
from Backend.board_generator import fp_resources, tp_resources, generate_board, render_board

fp, tp, exp, help = st.tabs(["4-Person", "2-Person", "Expansion", "Help"])

@st.cache_data
def load_board_images():
  TILE_SIZE = 120  
  img_dict = {}
  
  for file in st.session_state["image_files"]:
    file_base = file.split("/")[-1].replace(".png","")
    img_load = Image.open(file).convert("RGBA")
    img_load = img_load.resize((TILE_SIZE, TILE_SIZE))
    img_load = img_load.rotate(15, expand=False, resample=Image.Resampling.BICUBIC)
    img_dict[file_base] = img_load

  return img_dict

if "image_files" not in st.session_state:
  img_files = glob.glob("./Images/*.png")
  st.session_state.image_files = img_files

if "img_stem" not in st.session_state:
  st.session_state.img_stem = [f.split("/")[-1] for f in st.session_state.image_files]

if "board_images" not in st.session_state:
  st.session_state.board_images = load_board_images()

st.write(st.session_state.board_images.keys())

with fp:
  st.header("Catan Board Generator - 4 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      board = generate_board(fp_resources)
      board_render = render_board(board, st.session_state.board_images)
      st.image(board_render)
      
