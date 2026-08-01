import streamlit as st
import random
import glob
from PIL import Image

tp, fp, exp, help = st.tabs(["2-Person", "4-Person", "Expansion", "Help"])

if "image_files" not in st.session_state:
  img_files = glob.glob("./Images/*.png")
  st.session_state.image_files = img_files

if "img_stem" not in st.session_state:
  st.session_state.img_stem = [f.split("/")[-1] for f in st.session_state.image_files]

@st.cache_data
def load_board_images():
  img_dict = {}
  for file in st.session_state["image_files"]:
    file_base = file.split("/")[-1]
    img_load = Image.open(file)
    img_dict[file_base] = img_load

  return img_dict

board_images = load_board_images()

with tp:
  game_container = st.container()
  with game_container:
    st.header("Catan Board Generator - 2 Player")
    generate_btn = st.button("Generate Board")
    if generate_btn:
      options = st.session_state.img_stem
      choice = random.choice(options)
      st.image(board_images[choice])
      
