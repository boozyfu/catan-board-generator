import streamlit as st
import random
import glob
from PIL import Image
from Backend.board_generator import fp_resources, tp_resources, create_catan_board_svg 

tile_size = 120
fp, tp, exp, help = st.tabs(["4-Person", "2-Person", "Expansion", "Help"])

if "image_files" not in st.session_state:
  st.session_state["image_files"] = glob.glob("./Images/*.png")


with fp:
  st.header("Catan Board Generator - 4 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      #game_board = create_catan_board(fp_resources, "fp")
      #st.image(game_board)
      board_svg = create_catan_board_svg(fp_resources, "fp", tile_size=150, font_size=20)
      st.write(board_svg, unsafe_allow_html=True)
