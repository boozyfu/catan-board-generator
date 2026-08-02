import streamlit as st
import random
import glob
from PIL import Image
from Backend.board_generator import fp_resources, tp_resources, create_catan_board, render_image

tile_size = 120
fp, tp, exp, help = st.tabs(["4-Person", "2-Person", "Expansion", "Help"])

if "image_files" not in st.session_state:
  st.session_state["image_files"] = glob.glob("./Images/*.png")


with fp:
  st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=5.0, user-scalable=yes, maximum-scale=5.0">
    """,
    unsafe_allow_html=True
)
  st.header("Catan Board Generator - 4 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      game_board = create_catan_board(fp_resources, "fp")
      render_image(game_board)

with tp:
  st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=5.0, user-scalable=yes, maximum-scale=5.0">
    """,
    unsafe_allow_html=True
)
  st.header("Catan Board Generator - 2 Player")
  game_container = st.container()
  with game_container:
    with st.bottom:
      generate_btn = st.button("Generate Board")
    if generate_btn:
      game_board = create_catan_board(tp_resources, "tp")
      render_image(game_board)


  
