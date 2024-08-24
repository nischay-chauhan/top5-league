import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data

data = load_data('./dataset/test.csv')

player_names = data["Player"].unique()

st.header("Football Players Stats in Top 5 Leagues 2023/24")

selected_player = st.selectbox(
    "Select a player:",
    player_names
)

stats_options = [
    'Gls', 'Ast', 'xG', 'xAG', 'Gls_90', 'Ast_90'
]

selected_stats = st.multiselect(
    "Select statistics to display:",
    stats_options,
    default=['Gls', 'Ast']
)

chart_type = st.selectbox(
    "Choose the type of chart to display:",
    ["Pie Chart", "Bar Chart", "Line Chart"]
)

if selected_player:
    filtered_data = data[data["Player"].str.strip().str.lower() == selected_player.strip().lower()]

    if not filtered_data.empty:
        st.markdown(f"<h2 style='color:#FFA500;'>Statistics for {selected_player.title()}</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col7, col8, col9 = st.columns(3)

        col1.markdown(f"<p style='font-size:20px;'>Serial Number</p><h3>{filtered_data.iloc[0]['Rk']}</h3>", unsafe_allow_html=True)
        col2.markdown(f"<p style='font-size:20px;'>Nation</p><h3>{filtered_data.iloc[0]['Nation']}</h3>", unsafe_allow_html=True)
        col3.markdown(f"<p style='font-size:20px;'>Position</p><h3>{filtered_data.iloc[0]['Pos']}</h3>", unsafe_allow_html=True)
        
        col4.markdown(f"<p style='font-size:20px;'>Squad</p><h3>{filtered_data.iloc[0]['Squad']}</h3>", unsafe_allow_html=True)
        col5.markdown(f"<p style='font-size:20px;'>Competition</p><h3>{filtered_data.iloc[0]['Comp']}</h3>", unsafe_allow_html=True)
        col6.markdown(f"<p style='font-size:20px;'>Age</p><h3>{filtered_data.iloc[0]['Age']}</h3>", unsafe_allow_html=True)
        
        col7.markdown(f"<p style='font-size:20px;'>Matches Played</p><h3>{filtered_data.iloc[0]['MP']}</h3>", unsafe_allow_html=True)
        col8.markdown(f"<p style='font-size:20px;'>Goals</p><h3>{filtered_data.iloc[0]['Gls']}</h3>", unsafe_allow_html=True)
        col9.markdown(f"<p style='font-size:20px;'>Assists</p><h3>{filtered_data.iloc[0]['Ast']}</h3>", unsafe_allow_html=True)

        st.subheader("Full Statistics Table")
        st.dataframe(filtered_data, use_container_width=True)

        st.markdown("------------------------")  

        stats = {k: filtered_data.iloc[0][k] for k in selected_stats if k in filtered_data.columns}

        if chart_type == "Pie Chart":
            st.subheader(f"Statistics as Pie Chart")
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(stats.values(), labels=stats.keys(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
            ax.set_title("Statistics Distribution", fontsize=16)
            st.pyplot(fig)

        elif chart_type == "Bar Chart":
            st.subheader(f"Statistics as Bar Chart")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=list(stats.keys()), y=list(stats.values()), ax=ax, palette="pastel", ci=None)
            ax.set_title("Statistics Comparison", fontsize=16)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)

        elif chart_type == "Line Chart":
            st.subheader(f"Statistics as Line Chart")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=list(stats.keys()), y=list(stats.values()), marker='o', ax=ax, palette="pastel")
            ax.set_title("Statistics Trend", fontsize=16)
            ax.set_xticks(range(len(stats)))
            ax.set_xticklabels(stats.keys(), rotation=45, ha='right')
            st.pyplot(fig)

    else:
        st.write("No player found with that name.")

