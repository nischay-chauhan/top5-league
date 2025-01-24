import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data
import numpy as np

# Set page configuration with responsive layout
st.set_page_config(
    page_title="Football Stats Explorer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapse sidebar by default on mobile
)

# Custom CSS with better text contrast
st.markdown("""
    <style>
    /* Modern color palette */
    :root {
        --primary-color: #2C3E50;
        --secondary-color: #3498DB;
        --accent-color: #E74C3C;
        --background-color: #1a1a1a;
        --card-background: #2d2d2d;
        --text-color: #FFFFFF;
        --text-muted: #B0B0B0;
        --hover-color: #2980B9;
        --border-color: #404040;
    }

    /* Global styles */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Headers */
    h1 {
        font-size: min(2.5rem, 4vw);
        border-bottom: 3px solid var(--secondary-color);
        padding-bottom: 0.5rem;
        color: var(--text-color);
        font-weight: 600;
        margin-bottom: 1rem;
        max-width: 800px;
    }

    h2 {
        font-size: min(2rem, 3vw);
        color: var(--secondary-color);
        font-weight: 600;
        margin-bottom: 1rem;
        max-width: 800px;
    }

    h3 {
        font-size: min(1.5rem, 2.5vw);
        color: var(--text-color);
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Stat cards */
    .stat-card {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: min(1.5rem, 2vw);
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
        border-left: 4px solid var(--secondary-color);
        max-width: 300px;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
    }

    .stat-card p {
        color: var(--text-muted);
        font-size: min(0.9rem, 1.5vw);
        margin-bottom: 0.5rem;
    }

    .stat-card h3 {
        color: var(--text-color);
        font-size: min(1.4rem, 2vw);
        margin: 0;
        font-weight: 600;
    }

    /* DataFrames */
    .dataframe {
        background-color: var(--card-background);
        color: var(--text-color);
        max-width: 1400px !important;
        margin: 0 auto;
        font-size: 1.1rem !important;
        border: 1px solid var(--border-color);
    }

    .dataframe th {
        background-color: var(--primary-color);
        color: var(--text-color);
        padding: 1.2rem !important;
        border-bottom: 2px solid var(--border-color);
        font-size: 1.2rem !important;
    }

    .dataframe td {
        color: var(--text-color);
        padding: 1.2rem !important;
        border-bottom: 1px solid var(--border-color);
        font-size: 1.1rem !important;
    }

    /* Metrics */
    .css-1r6slb0 {
        background-color: var(--card-background);
        color: var(--text-color);
    }

    .css-1r6slb0 label {
        color: var(--text-muted);
    }

    /* Selectbox */
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--card-background);
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }

    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--secondary-color);
    }

    .stSelectbox [data-baseweb="select"] > div {
        color: var(--text-color);
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--card-background);
    }

    .css-1d391kg .sidebar-content {
        background-color: var(--card-background);
        color: var(--text-color);
    }

    /* Charts */
    .stPlot {
        background-color: var(--card-background);
        padding: 0.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        max-width: 500px !important;
        margin: 0 auto;
    }

    /* Comparison section */
    .comparison-container {
        max-width: 800px;
        margin: 0 auto;
        background-color: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }

    .comparison-metric {
        color: var(--text-color);
        background-color: var(--card-background);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--secondary-color);
        border-radius: 4px;
    }

    /* Streamlit elements */
    .stMarkdown {
        color: var(--text-color);
    }

    .stTextInput > div > div {
        background-color: var(--card-background);
        color: var(--text-color);
    }

    .stTextInput > div > div:hover {
        border-color: var(--secondary-color);
    }

    /* Footer */
    footer {
        color: var(--text-muted);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def get_data():
    return load_data('./dataset/test.csv')

data = get_data()
player_names = sorted(data["Player"].unique())

# Sidebar for filters
st.sidebar.header("⚙️ Filters")
league_filter = st.sidebar.multiselect(
    "Filter by League:",
    sorted(data["Comp"].unique()),
    default=[]
)

position_filter = st.sidebar.multiselect(
    "Filter by Position:",
    sorted(data["Pos"].unique()),
    default=[]
)

# Apply filters to player list
filtered_players = data
if league_filter:
    filtered_players = filtered_players[filtered_players["Comp"].isin(league_filter)]
if position_filter:
    filtered_players = filtered_players[filtered_players["Pos"].isin(position_filter)]
filtered_player_names = sorted(filtered_players["Player"].unique())

# Main content
st.title("⚽ Football Players Stats Explorer - Top 5 Leagues 2023/24")
st.markdown("Explore and analyze player statistics from the top football leagues.")

# Player selection with search
selected_player = st.selectbox(
    "🔍 Search and select a player:",
    filtered_player_names
)

# Enhanced statistics options
stats_options = {
    'Gls': 'Goals',
    'Ast': 'Assists',
    'xG': 'Expected Goals',
    'xAG': 'Expected Assists',
    'Gls_90': 'Goals per 90',
    'Ast_90': 'Assists per 90',
    'MP': 'Matches Played',
    'Min': 'Minutes Played'
}

selected_stats = st.multiselect(
    "📊 Select statistics to display:",
    list(stats_options.keys()),
    default=['Gls', 'Ast', 'xG', 'xAG'],
    format_func=lambda x: stats_options[x]
)

# Visualization options
col1, col2 = st.columns(2)
with col1:
    chart_type = st.selectbox(
        "📈 Choose visualization type:",
        ["Bar Chart", "Pie Chart", "Line Chart", "Radar Chart"]
    )
with col2:
    color_theme = st.selectbox(
        "🎨 Select color theme:",
        ["pastel", "deep", "muted", "colorblind", "dark"]
    )

if selected_player:
    filtered_data = data[data["Player"].str.strip().str.lower() == selected_player.strip().lower()]

    if not filtered_data.empty:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown(f"## 👤 {selected_player}'s Profile")
        
        # Key stats in cards
        key_stats = [
            ("🌍 Nation", "Nation", "#3498DB"),
            ("👕 Position", "Pos", "#E74C3C"),
            ("⚽ Team", "Squad", "#2ECC71"),
            ("🏆 League", "Comp", "#F1C40F")
        ]
        
        # Responsive grid for stats with better sizing
        cols = st.columns(4)
        for i, (label, key, color) in enumerate(key_stats):
            with cols[i]:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: {color}">
                    <p style='font-size: min(0.9rem, 1.5vw);'>{label}</p>
                    <h3 style="color: {color}">{filtered_data.iloc[0][key]}</h3>
                </div>
                """, unsafe_allow_html=True)

        # Performance metrics with controlled sizing
        st.markdown("## 📊 Performance Metrics")
        
        if selected_stats:
            stats = {k: filtered_data.iloc[0][k] for k in selected_stats if k in filtered_data.columns}
            
            # Adjust figure sizes based on screen size
            fig_width = min(6, len(stats) * 1)  # Reduced from 8 to 6
            fig_height = min(4, fig_width * 0.6)  # Reduced from 5 to 4
            
            # Custom color palettes for charts
            custom_palettes = {
                "Bar Chart": ["#3498DB", "#E74C3C", "#2ECC71", "#F1C40F", "#9B59B6", "#1ABC9C"],
                "Pie Chart": ["#3498DB", "#E74C3C", "#2ECC71", "#F1C40F", "#9B59B6", "#1ABC9C"],
                "Line Chart": "#3498DB",
                "Radar Chart": "#3498DB"
            }
            
            if chart_type == "Bar Chart":
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                sns.barplot(x=list(stats.keys()), y=list(stats.values()), ax=ax, 
                          palette=custom_palettes["Bar Chart"])
                plt.xticks(rotation=45, ha='right', color='white')
                plt.yticks(color='white')
                ax.set_facecolor('#2d2d2d')
                fig.patch.set_facecolor('#1a1a1a')
                ax.spines['bottom'].set_color('#404040')
                ax.spines['top'].set_color('#404040')
                ax.spines['left'].set_color('#404040')
                ax.spines['right'].set_color('#404040')
                ax.tick_params(colors='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                plt.title(f"{selected_player}'s Statistics", 
                         pad=20, fontsize=min(16, fig_width * 1.2), 
                         fontweight='bold', color='white')
                plt.tight_layout()
                st.pyplot(fig)
                
            elif chart_type == "Pie Chart":
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                plt.pie(stats.values(), labels=[stats_options[k] for k in stats.keys()], 
                       autopct='%1.1f%%', colors=custom_palettes["Pie Chart"])
                plt.title(f"{selected_player}'s Statistics Distribution")
                ax.set_facecolor('#2d2d2d')
                fig.patch.set_facecolor('#1a1a1a')
                st.pyplot(fig)
                
            elif chart_type == "Line Chart":
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                plt.plot(list(stats.keys()), list(stats.values()), marker='o', 
                        color=sns.color_palette(custom_palettes["Line Chart"])[0])
                plt.xticks(rotation=45, ha='right', color='white')
                plt.yticks(color='white')
                ax.set_facecolor('#2d2d2d')
                fig.patch.set_facecolor('#1a1a1a')
                ax.spines['bottom'].set_color('#404040')
                ax.spines['top'].set_color('#404040')
                ax.spines['left'].set_color('#404040')
                ax.spines['right'].set_color('#404040')
                ax.tick_params(colors='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                plt.title(f"{selected_player}'s Statistics Trend", 
                         pad=20, fontsize=min(16, fig_width * 1.2), 
                         fontweight='bold', color='white')
                plt.tight_layout()
                st.pyplot(fig)
                
            elif chart_type == "Radar Chart":
                # Radar chart implementation
                angles = np.linspace(0, 2*np.pi, len(stats), endpoint=False)
                values = list(stats.values())
                values += values[:1]
                angles = np.concatenate((angles, [angles[0]]))
                
                fig, ax = plt.subplots(figsize=(fig_width, fig_height), subplot_kw=dict(projection='polar'))
                ax.plot(angles, values)
                ax.fill(angles, values, alpha=0.25)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(list(stats.keys()))
                plt.title(f"{selected_player}'s Statistics Radar", 
                         pad=20, fontsize=min(16, fig_width * 1.2), 
                         fontweight='bold', color='white')
                ax.set_facecolor('#2d2d2d')
                fig.patch.set_facecolor('#1a1a1a')
                ax.spines['bottom'].set_color('#404040')
                ax.spines['top'].set_color('#404040')
                ax.spines['left'].set_color('#404040')
                ax.spines['right'].set_color('#404040')
                ax.tick_params(colors='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

        # Detailed stats table with controlled width
        st.markdown("<div style='max-width: 1000px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown("## 📋 Detailed Statistics")
        st.dataframe(
            filtered_data.style.highlight_max(axis=0, subset=['Gls', 'Ast', 'xG', 'xAG']),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Player comparison with controlled width
        st.markdown("<div class='comparison-container'>", unsafe_allow_html=True)
        st.markdown("## 🔄 Compare with another player")
        comparison_player = st.selectbox(
            "Select a player to compare with:",
            [p for p in filtered_player_names if p != selected_player]
        )
        
        if comparison_player:
            comp_data = data[data["Player"] == comparison_player].iloc[0]
            
            st.markdown("### Head-to-head comparison")
            # Show comparisons in a vertical layout on mobile
            for stat in selected_stats:
                st.markdown(f"**{stats_options[stat]}**")
                col1, col2 = st.columns(2)
                player1_val = filtered_data.iloc[0][stat]
                player2_val = comp_data[stat]
                
                col1.metric(
                    selected_player, 
                    f"{player1_val:.2f}",
                    None,
                    help=f"{selected_player}'s {stats_options[stat]}"
                )
                col2.metric(
                    comparison_player,
                    f"{player2_val:.2f}",
                    f"{((player2_val - player1_val) / player1_val * 100):.1f}%",
                    help=f"{comparison_player}'s {stats_options[stat]}"
                )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("No player found with that name.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | Data source: Top 5 Leagues 2023/24")

# Helper function for responsive font sizes
def clamp(min_size, max_size):
    return max(min(max_size, 14), min_size)  # Default to 14px if between min and max
