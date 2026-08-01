import streamlit as st
import random

tp, fp, exp, help = st.tabs(["2-Person", "4-Person", "Expansion", "Help"])

with tp:
  game_container = st.container()
  with game_container:
    st.header("Catan Board Generator - 2 Player")
    generate_btn = st.button("Generate Board")
    if generate_btn:
      options = [1,2,3,4,5]
      choice = random.choice(options)
      st.write(choice)
