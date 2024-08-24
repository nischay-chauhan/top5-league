import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data

data = load_data('./dataset/test.csv')

st.header("Compare Players Stats")

player_names = data["Player"].unique()
selected_players = st.multiselect(
    "Select two players to compare:",
    player_names,
    default=[player_names[0], player_names[1]]
)

if len(selected_players) == 2:
    player_data = data[data["Player"].isin(selected_players)]
    player_data.set_index('Player', inplace=True)
    
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
        ["Bar Chart", "Line Chart"]
    )

    if not player_data.empty:
        st.subheader("Comparison of Statistics")

        stats_data = player_data[selected_stats]

        if chart_type == "Bar Chart":
            st.subheader("Statistics Comparison as Bar Chart")
            fig, ax = plt.subplots(figsize=(10, 6))
            stats_data.plot(kind='bar', ax=ax, color=sns.color_palette("pastel", len(selected_stats)))
            ax.set_title("Statistics Comparison")
            ax.set_xticklabels(stats_data.index, rotation=45, ha='right')
            st.pyplot(fig)

        elif chart_type == "Line Chart":
            st.subheader("Statistics Comparison as Line Chart")
            fig, ax = plt.subplots(figsize=(10, 6))
            for stat in selected_stats:
                sns.lineplot(data=stats_data, x=stats_data.index, y=stat, marker='o', ax=ax, label=stat)
            ax.set_title("Statistics Trend")
            ax.set_xticklabels(stats_data.index, rotation=45, ha='right')
            ax.legend()
            st.pyplot(fig)

    else:
        st.write("No data available for selected players.")
else:
    st.write("Please select exactly two players for comparison.")
