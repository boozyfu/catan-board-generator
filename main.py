import streamlit as st
import random
import glob
from PIL import Image
from Backend.board_generator import fp_resources, tp_resources, display_board 

tile_size = 120
fp, tp, exp, help = st.tabs(["4-Person", "2-Person", "Expansion", "Help"])

with fp:
  st.header("Catan Board Generator - 4 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      display_board(fp_resources)
