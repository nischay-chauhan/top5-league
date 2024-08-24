import streamlit as st
pg = st.navigation([st.Page("main.py") , st.Page("compare_players.py")])

pg.run()