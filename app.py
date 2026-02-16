import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scraper import scrape_all_data

# Page config
st.set_page_config(
    page_title="Edison Soccer Analytics", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Off-white background, Edison colors, fixed contrast
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Force light theme with off-white background */
    .stApp {
        background-color: #fafaf8 !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        font-weight: 800 !important;
        font-size: 2.75rem !important;
        background: linear-gradient(135deg, #DC143C 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem !important;
        text-align: center;
    }
    
    h2 {
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        color: #DC143C !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        color: #8B0000 !important;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .coach-name {
        text-align: center;
        font-size: 1.1rem;
        color: #DC143C;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        color: #DC143C !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        color: #FFD700 !important;
        font-weight: 600 !important;
    }
    
    /* Metric container styling */
    [data-testid="metric-container"] {
        background-color: white;
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px solid #fee;
        box-shadow: 0 2px 8px rgba(220, 20, 60, 0.08);
    }
    
    /* Tables */
    .dataframe {
        border: none !important;
        font-size: 0.9rem !important;
        background-color: white !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em !important;
        padding: 14px !important;
        border: none !important;
    }
    
    .dataframe tbody tr td {
        padding: 12px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        background-color: white !important;
        color: #1a1a1a !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #fff5f5 !important;
    }
    
    /* Make sure dataframe wrapper has white background */
    [data-testid="stDataFrame"] {
        background-color: white !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: white;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        color: #64748b;
        border-bottom: 3px solid transparent;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #DC143C !important;
        border-bottom-color: #FFD700 !important;
        background-color: #fff5f5;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #FFD700 !important;
        background-color: #fffbeb !important;
        padding: 1rem 1.5rem;
        color: #1a1a1a !important;
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
        border-color: #FFD700 !important;
    }
    
    /* Charts */
    .js-plotly-plot {
        border-radius: 12px;
        background-color: white !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        padding: 0.5rem;
    }
    
    /* Text elements */
    .stMarkdown, p, span, div, label {
        color: #1a1a1a !important;
    }
    
    /* Accent boxes */
    .accent-box {
        background-color: white;
        border-left: 4px solid #DC143C;
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(220, 20, 60, 0.08);
    }
    
    /* Footer */
    .caption {
        text-align: center;
        color: #64748b !important;
        font-size: 0.875rem;
        margin-top: 3rem;
        padding: 1.5rem;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #DC143C !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1>⚽ Edison High School Soccer</h1>
    <div class="subtitle">Advanced Analytics Dashboard • 2025-2026 Season</div>
""", unsafe_allow_html=True)

# Load all data
with st.spinner("🔄 Loading data from nj.com..."):
    data = scrape_all_data()

if not data or not data['current_stats']:
    st.error("❌ Failed to load data. Please refresh the page.")
    st.stop()

# Extract data
current_field = data['current_stats']['field_players']
current_goalies = data['current_stats']['goalies']
prev_field = data['previous_stats']['field_players'] if data['previous_stats'] else pd.DataFrame()
prev_goalies = data['previous_stats']['goalies'] if data['previous_stats'] else pd.DataFrame()
fixtures = data['fixtures']['games']
roster = data['roster']
coach = data['fixtures']['coach']

# Display coach
st.markdown(f'<div class="coach-name">Head Coach: {coach}</div>', unsafe_allow_html=True)

# Success message
st.success(f"✅ Loaded {len(current_field)} players • {len(fixtures)} games • {len(roster)} roster members", icon="✅")

# Top metrics
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Team Goals", f"{current_field['Goals'].sum()}", delta=f"+{current_field['Goals'].sum() - (prev_field['Goals'].sum() if not prev_field.empty else 0)}")

with col2:
    st.metric("Team Assists", f"{current_field['Assists'].sum()}", delta=f"+{current_field['Assists'].sum() - (prev_field['Assists'].sum() if not prev_field.empty else 0)}")

with col3:
    st.metric("Total Saves", f"{current_goalies['Saves'].sum()}")

with col4:
    wins = len(fixtures[fixtures['Outcome'] == 'W'])
    losses = len(fixtures[fixtures['Outcome'] == 'L'])
    st.metric("Record", f"{wins}-{losses}")

with col5:
    top_scorer = current_field.loc[current_field['Goals'].idxmax()]
    st.metric("Top Scorer", top_scorer['Player'].split()[0], delta=f"{top_scorer['Goals']}G")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["⚽ Field Players", "🧤 Goalkeepers", "📅 Schedule", "👥 Roster", "📊 Year Comparison", "🎯 Team Analysis"])

# TAB 1: Field Players
with tabs[0]:
    st.markdown("### Field Player Statistics")
    
    sort_col1, sort_col2 = st.columns([3, 1])
    with sort_col2:
        sort_by = st.selectbox("Sort by", ["Goals", "Assists", "Points"], key="sort_field")
    
    field_sorted = current_field.sort_values(sort_by, ascending=False)
    
    st.dataframe(field_sorted, use_container_width=True, height=400, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Top 10 Scorers")
        top_scorers = field_sorted.head(10)
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=top_scorers['Goals'],
                y=top_scorers['Player'],
                orientation='h',
                marker=dict(
                    color=['#DC143C', '#E31C42', '#EA2348', '#F12A4E', '#F73154', 
                           '#FE385A', '#FF5270', '#FF6C86', '#FF869C', '#FFD700'][:len(top_scorers)],
                    line=dict(color='white', width=2)
                ),
                text=top_scorers['Goals'],
                textposition='outside',
                textfont=dict(size=14, color='#1a1a1a', family='Inter')
            )
        ])
        
        fig1.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Goals'),
            yaxis=dict(autorange="reversed"),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### Goals vs Assists")
        
        fig2 = go.Figure(data=[
            go.Scatter(
                x=current_field['Assists'],
                y=current_field['Goals'],
                mode='markers',
                marker=dict(
                    size=current_field['Points']*3 + 8,
                    color=current_field['Points'],
                    colorscale=[[0, '#FFD700'], [0.5, '#DC143C'], [1, '#8B0000']],
                    showscale=True,
                    colorbar=dict(title="Points"),
                    line=dict(width=2, color='white')
                ),
                text=current_field['Player'],
                hovertemplate='<b>%{text}</b><br>Goals: %{y}<br>Assists: %{x}<extra></extra>'
            )
        ])
        
        fig2.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Assists'),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Goals'),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig2, use_container_width=True)

# TAB 2: Goalkeepers
with tabs[1]:
    st.markdown("### Goalkeeper Statistics")
    
    current_goalies['Saves Per Game'] = current_goalies.apply(
        lambda x: round(x['Saves'] / x['Games Played'], 2) if x['Games Played'] > 0 else 0, axis=1
    )
    
    st.dataframe(current_goalies, use_container_width=True, height=300, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Total Saves")
        
        fig3 = go.Figure(data=[
            go.Bar(
                x=current_goalies['Player'],
                y=current_goalies['Saves'],
                marker=dict(
                    color=['#DC143C', '#E92952', '#FFD700', '#F73F68'][:len(current_goalies)],
                    line=dict(color='white', width=2)
                ),
                text=current_goalies['Saves'],
                textposition='outside',
                textfont=dict(color='#1a1a1a')
            )
        ])
        
        fig3.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### Saves Per Game Average")
        
        fig4 = go.Figure(data=[
            go.Bar(
                x=current_goalies['Player'],
                y=current_goalies['Saves Per Game'],
                marker=dict(
                    color=['#FFD700', '#DC143C', '#E92952', '#F73F68'][:len(current_goalies)],
                    line=dict(color='white', width=2)
                ),
                text=current_goalies['Saves Per Game'],
                textposition='outside',
                textfont=dict(color='#1a1a1a')
            )
        ])
        
        fig4.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig4, use_container_width=True)

# TAB 3: Schedule
with tabs[2]:
    st.markdown("### 2025-2026 Schedule & Results")
    
    if not fixtures.empty:
        # Clean up fixtures data
        fixtures['Opponent'] = fixtures['Opponent'].str.replace('\n', ' ').str.strip()
        fixtures['Result'] = fixtures['Result'].str.replace('\n', ' ').str.strip()
        
        # Display full schedule
        st.dataframe(fixtures, use_container_width=True, height=500, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Win/Loss visualization
        outcome_counts = fixtures['Outcome'].value_counts()
        
        fig_schedule = go.Figure(data=[
            go.Pie(
                labels=outcome_counts.index,
                values=outcome_counts.values,
                hole=0.4,
                marker=dict(colors=['#DC143C', '#8B0000', '#FFD700']),
                textfont=dict(size=16, color='white', family='Inter')
            )
        ])
        
        fig_schedule.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title=dict(text="Season Record", font=dict(size=20, color='#1a1a1a')),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig_schedule, use_container_width=True)
    else:
        st.info("No schedule data available")

# TAB 4: Roster
with tabs[3]:
    st.markdown("### 2025-2026 Team Roster")
    
    if not roster.empty:
        # Clean roster if needed
        st.dataframe(roster, use_container_width=True, height=600, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Position breakdown
        if 'Position' in roster.columns:
            st.markdown("#### Team Composition by Position")
            
            # Count positions (some players have multiple)
            position_counts = {}
            for pos in roster['Position']:
                positions = str(pos).split(',')
                for p in positions:
                    p = p.strip()
                    if p in position_counts:
                        position_counts[p] += 1
                    else:
                        position_counts[p] = 1
            
            fig_positions = go.Figure(data=[
                go.Bar(
                    x=list(position_counts.keys()),
                    y=list(position_counts.values()),
                    marker=dict(color='#DC143C', line=dict(color='white', width=2)),
                    text=list(position_counts.values()),
                    textposition='outside',
                    textfont=dict(color='#1a1a1a')
                )
            ])
            
            fig_positions.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(title='Position'),
                yaxis=dict(title='Players', showgrid=True, gridcolor='#f1f5f9'),
                font=dict(color='#1a1a1a')
            )
            
            st.plotly_chart(fig_positions, use_container_width=True)
    else:
        st.info("No roster data available")

# TAB 5: Year Comparison
with tabs[4]:
    st.markdown("### Year-Over-Year Comparison")
    
    if not prev_field.empty:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### Total Goals Comparison")
            
            comparison_data = pd.DataFrame({
                'Season': ['2024-2025', '2025-2026'],
                'Goals': [prev_field['Goals'].sum(), current_field['Goals'].sum()]
            })
            
            fig_goals_compare = go.Figure(data=[
                go.Bar(
                    x=comparison_data['Season'],
                    y=comparison_data['Goals'],
                    marker=dict(color=['#8B0000', '#DC143C'], line=dict(color='white', width=2)),
                    text=comparison_data['Goals'],
                    textposition='outside',
                    textfont=dict(size=18, color='#1a1a1a')
                )
            ])
            
            fig_goals_compare.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
                font=dict(color='#1a1a1a')
            )
            
            st.plotly_chart(fig_goals_compare, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### Total Assists Comparison")
            
            comparison_assists = pd.DataFrame({
                'Season': ['2024-2025', '2025-2026'],
                'Assists': [prev_field['Assists'].sum(), current_field['Assists'].sum()]
            })
            
            fig_assists_compare = go.Figure(data=[
                go.Bar(
                    x=comparison_assists['Season'],
                    y=comparison_assists['Assists'],
                    marker=dict(color=['#FFB700', '#FFD700'], line=dict(color='white', width=2)),
                    text=comparison_assists['Assists'],
                    textposition='outside',
                    textfont=dict(size=18, color='#1a1a1a')
                )
            ])
            
            fig_assists_compare.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
                font=dict(color='#1a1a1a')
            )
            
            st.plotly_chart(fig_assists_compare, use_container_width=True)
        
        # Returning players comparison
        st.markdown("#### Returning Player Performance")
        
        # Find players in both years
        prev_players = set(prev_field['Player'].str.strip().str.lower())
        returning = current_field[current_field['Player'].str.strip().str.lower().isin(prev_players)].copy()
        
        if not returning.empty:
            st.markdown(f"**{len(returning)} returning players from last season**")
            
            # Show their stats
            returning_sorted = returning.sort_values('Goals', ascending=False)
            st.dataframe(returning_sorted[['Player', 'Goals', 'Assists', 'Points']], use_container_width=True, hide_index=True)
        else:
            st.info("No returning players found in current stats")
    else:
        st.info("Previous year data not available for comparison")

# TAB 6: Team Analysis
with tabs[5]:
    st.markdown("### Team Overview & Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown('<div class="accent-box">', unsafe_allow_html=True)
        st.markdown("**🌟 Top Performers**")
        top_3 = current_field.nlargest(3, 'Goals')[['Player', 'Goals', 'Assists']]
        for idx, row in top_3.iterrows():
            st.markdown(f"• **{row['Player']}**: {row['Goals']}G, {row['Assists']}A")
        
        st.markdown("<br>**🧤 Best Goalkeeper**", unsafe_allow_html=True)
        best_gk = current_goalies.loc[current_goalies['Saves'].idxmax()]
        st.markdown(f"• **{best_gk['Player']}**: {best_gk['Saves']} saves in {best_gk['Games Played']} games")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with insight_col2:
        st.markdown('<div class="accent-box">', unsafe_allow_html=True)
        st.markdown("**👥 Team Composition**")
        st.markdown(f"• Total Players: {len(current_field) + len(current_goalies)}")
        st.markdown(f"• Field Players: {len(current_field)}")
        st.markdown(f"• Goalkeepers: {len(current_goalies)}")
        
        scoring_players = len(current_field[current_field['Goals'] > 0])
        st.markdown(f"• Players with Goals: {scoring_players} ({round(scoring_players/len(current_field)*100)}%)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Points Distribution")
        
        fig5 = go.Figure(data=[
            go.Histogram(
                x=current_field['Points'],
                nbinsx=15,
                marker=dict(color='#DC143C', line=dict(color='white', width=1))
            )
        ])
        
        fig5.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Points', showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title='Players', showgrid=True, gridcolor='#f1f5f9'),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig5, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### Goals Distribution")
        
        fig6 = go.Figure(data=[
            go.Histogram(
                x=current_field['Goals'],
                nbinsx=12,
                marker=dict(color='#FFD700', line=dict(color='white', width=1))
            )
        ])
        
        fig6.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Goals', showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title='Players', showgrid=True, gridcolor='#f1f5f9'),
            font=dict(color='#1a1a1a')
        )
        
        st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("""
    <div class="caption">
        <strong style="background: linear-gradient(135deg, #DC143C 0%, #FFD700 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Edison Eagles Soccer Analytics</strong><br>
        Real-time data from nj.com • Built by Prayag Patel<br>
        <span style="color: #DC143C;">●</span> Live Updates <span style="color: #FFD700;">●</span> 2025-2026 Season
    </div>
""", unsafe_allow_html=True)
