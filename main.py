import streamlit as st
import random

main, help = st.tabs["Main", "Help"]

with main:
  game_container = st.container()
  with game_container:
    generate_btn = st.button("Generate Board")
    if generate_btn:
      options = [1,2,3,4,5]
      choice = random.choice(options)
      st.write(choice)
