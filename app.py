import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="SRH Analytics Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── THEME & CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&family=Rajdhani:wght@500;600;700&display=swap');

:root {
    --srh-orange: #F26522;
    --srh-orange-light: #FF8C42;
    --srh-orange-glow: rgba(242, 101, 34, 0.3);
    --bg-primary: #050505;
    --bg-secondary: #0f0f0f;
    --bg-card: #141414;
    --bg-card-hover: #1a1a1a;
    --border: rgba(242, 101, 34, 0.2);
    --border-bright: rgba(242, 101, 34, 0.6);
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --text-muted: #555555;
}

html, body, .stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide streamlit defaults */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 2rem 2rem 2rem !important; max-width: 100% !important;}

/* ── HERO HEADER ── */
.hero {
    background: linear-gradient(135deg, #050505 0%, #1a0a00 50%, #050505 100%);
    border-bottom: 1px solid var(--border-bright);
    padding: 3rem 2rem 2rem 2rem;
    margin: -2rem -2rem 2rem -2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--srh-orange-glow) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    line-height: 0.9;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #ffffff 0%, var(--srh-orange) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    color: var(--text-secondary);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.hero-badge {
    display: inline-block;
    background: var(--srh-orange);
    color: #000;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 2px;
    margin-top: 1rem;
    text-transform: uppercase;
}

/* ── STAT CARDS ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--srh-orange);
}
.stat-card:hover {
    border-color: var(--border-bright);
    box-shadow: 0 0 30px var(--srh-orange-glow);
}
.stat-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: var(--srh-orange);
    line-height: 1;
    margin: 0;
}
.stat-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}
.stat-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
}

/* ── SECTION HEADERS ── */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 3px;
    color: var(--text-primary);
    border-left: 4px solid var(--srh-orange);
    padding-left: 1rem;
    margin: 2rem 0 1.5rem 0;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
    padding: 1rem 2rem !important;
    border-bottom: 3px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--srh-orange) !important;
    border-bottom: 3px solid var(--srh-orange) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 1.5rem 0 !important;
}

/* ── PLAYER CARDS ── */
.player-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.player-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--srh-orange), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.player-card:hover {
    border-color: var(--border-bright);
    box-shadow: 0 8px 32px var(--srh-orange-glow);
    transform: translateY(-4px);
}
.player-card:hover::after { opacity: 1; }
.player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 2px;
    color: var(--text-primary);
    margin: 0.5rem 0 0.25rem 0;
}
.player-role {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: var(--srh-orange);
    text-transform: uppercase;
}
.player-stat {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: var(--srh-orange);
}
.player-stat-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── DIVIDER ── */
.srh-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--srh-orange), transparent);
    margin: 2rem 0;
    opacity: 0.4;
}

/* ── PLOTLY CHARTS ── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ─────────────────────────────────────────────
@st.cache_data
def load_data():
    ball = pd.read_csv('ball_by_ball_data.csv')
    matches = pd.read_csv('ipl_matches_data.csv')
    players = pd.read_csv('players-data-updated.csv')
    teams = pd.read_csv('teams_data.csv')

    # Filter SRH (team_id = 2), 2013 onwards
    srh_matches = matches[
        ((matches['team1'] == 2) | (matches['team2'] == 2)) &
        (matches['season_id'] >= 2013)
    ].copy()

    srh_ball = ball[
        ((ball['team_batting'] == 2) | (ball['team_bowling'] == 2)) &
        (ball['season_id'] >= 2013)
    ].copy()

    return ball, matches, srh_matches, srh_ball, players

ball, matches, srh_matches, srh_ball, players = load_data()

# ── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-sub">🧡 Indian Premier League · 2013–2026</p>
    <h1 class="hero-title">SUNRISERS<br>HYDERABAD</h1>
    <p class="hero-sub">Analytics Dashboard</p>
    <span class="hero-badge">⚡ Rise of the Orange Army</span>
</div>
""", unsafe_allow_html=True)

# ── TOP LEVEL STATS ───────────────────────────────────────────
total_matches = len(srh_matches)
total_wins = (srh_matches['match_winner'] == 2).sum()
win_pct = round(total_wins / total_matches * 100, 1)
titles = 1  # 2016

c1, c2, c3, c4, c5 = st.columns(5)
stats = [
    (str(total_matches), "Matches Played", "IPL 2013–2026"),
    (str(total_wins), "Total Wins", f"{win_pct}% Win Rate"),
    ("1", "IPL Title", "Champions 2016 🏆"),
    ("13", "Seasons", "2013 to 2026"),
    ("187", "Players Used", "Across all seasons"),
]
for col, (num, label, sub) in zip([c1,c2,c3,c4,c5], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-number">{num}</p>
            <p class="stat-label">{label}</p>
            <p class="stat-sub">{sub}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📅  SEASON OVERVIEW",
    "🏏  BATTING",
    "🎯  BOWLING",
    "⭐  PLAYER SPOTLIGHT"
])
# ── TAB 1: SEASON OVERVIEW ────────────────────────────────────
with tab1:
    st.markdown('<p class="section-title">SEASON BY SEASON</p>', unsafe_allow_html=True)

    # Win/loss by season
    srh_matches['srh_won'] = srh_matches['match_winner'] == 2
    season_stats = srh_matches.groupby('season_id').agg(
        matches=('match_id', 'count'),
        wins=('srh_won', 'sum')
    ).reset_index()
    season_stats['losses'] = season_stats['matches'] - season_stats['wins']
    season_stats['win_pct'] = (season_stats['wins'] / season_stats['matches'] * 100).round(1)

    # Win/Loss bar chart
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=season_stats['season_id'],
        y=season_stats['wins'],
        name='Wins',
        marker_color='#F26522',
        marker_line_width=0,
    ))
    fig1.add_trace(go.Bar(
        x=season_stats['season_id'],
        y=season_stats['losses'],
        name='Losses',
        marker_color='#2a2a2a',
        marker_line_width=0,
    ))
    # Highlight 2016
    fig1.add_vline(x=2016, line_color='#F26522', line_dash='dash', opacity=0.5)
    fig1.add_annotation(x=2016, y=12, text="🏆 CHAMPIONS", 
                       font=dict(color='#F26522', size=12, family='Rajdhani'),
                       showarrow=False, yshift=10)
    fig1.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(showgrid=False, tickfont=dict(color='#a0a0a0')),
        yaxis=dict(showgrid=True, gridcolor='#1a1a1a', tickfont=dict(color='#a0a0a0')),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a0a0a0')),
        margin=dict(l=0, r=0, t=20, b=0),
        height=350,
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Win percentage line chart
    st.markdown('<p class="section-title">WIN PERCENTAGE TREND</p>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=season_stats['season_id'],
        y=season_stats['win_pct'],
        mode='lines+markers',
        line=dict(color='#F26522', width=3),
        marker=dict(size=8, color='#F26522', 
                   line=dict(color='#ffffff', width=2)),
        fill='tozeroy',
        fillcolor='rgba(242, 101, 34, 0.1)',
    ))
    fig2.add_hline(y=50, line_dash='dash', line_color='#555555', 
                  annotation_text='50% Baseline', 
                  annotation_font_color='#555555')
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(showgrid=False, tickfont=dict(color='#a0a0a0')),
        yaxis=dict(showgrid=True, gridcolor='#1a1a1a', 
                  tickfont=dict(color='#a0a0a0'), range=[0, 100]),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Best and worst seasons
    st.markdown('<p class="section-title">BEST & WORST SEASONS</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    best = season_stats.loc[season_stats['win_pct'].idxmax()]
    worst = season_stats.loc[season_stats['win_pct'].idxmin()]
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-label">🏆 Best Season</p>
            <p class="stat-number">{int(best['season_id'])}</p>
            <p class="stat-sub">{int(best['wins'])}W - {int(best['losses'])}L · {best['win_pct']}% Win Rate</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-label">📉 Toughest Season</p>
            <p class="stat-number">{int(worst['season_id'])}</p>
            <p class="stat-sub">{int(worst['wins'])}W - {int(worst['losses'])}L · {worst['win_pct']}% Win Rate</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">PERFORMANCE BY VENUE</p>', unsafe_allow_html=True)

    # Clean venues
    venue_map = {
        'Rajiv Gandhi International Stadium, Uppal': 'Rajiv Gandhi Stadium',
        'Rajiv Gandhi International Stadium, Uppal, Hyderabad': 'Rajiv Gandhi Stadium',
        'Rajiv Gandhi International Stadium': 'Rajiv Gandhi Stadium',
        'Wankhede Stadium, Mumbai': 'Wankhede Stadium',
        'MA Chidambaram Stadium, Chepauk, Chennai': 'Chepauk Stadium',
        'MA Chidambaram Stadium, Chepauk': 'Chepauk Stadium',
        'Feroz Shah Kotla': 'Arun Jaitley Stadium',
        'Feroz Shah Kotla, Delhi': 'Arun Jaitley Stadium',
    }
    srh_matches['venue_clean'] = srh_matches['venue'].replace(venue_map)
    srh_matches['venue_clean'] = srh_matches['venue_clean'].apply(
        lambda x: venue_map.get(x, x.split(',')[0].strip())
    )
    srh_matches['srh_won'] = srh_matches['match_winner'] == 2

    venue_stats = srh_matches.groupby('venue_clean').agg(
        matches=('match_id', 'count'),
        wins=('srh_won', 'sum')
    ).reset_index()
    venue_stats['win_pct'] = (venue_stats['wins'] / venue_stats['matches'] * 100).round(1)
    venue_stats['losses'] = venue_stats['matches'] - venue_stats['wins']
    venue_stats = venue_stats[venue_stats['matches'] >= 4].sort_values('win_pct', ascending=True)

    fig_venue = go.Figure()
    fig_venue.add_trace(go.Bar(
        y=venue_stats['venue_clean'],
        x=venue_stats['win_pct'],
        orientation='h',
        marker=dict(
            color=venue_stats['win_pct'],
            colorscale=[[0, '#1a1a1a'], [0.4, '#8B2500'], [1, '#F26522']],
            showscale=False,
        ),
        text=venue_stats['win_pct'].astype(str) + '%',
        textposition='outside',
        textfont=dict(color='#F26522', family='Rajdhani', size=12),
        customdata=venue_stats[['matches', 'wins', 'losses']].values,
        hovertemplate='<b>%{y}</b><br>Win Rate: %{x}%<br>Matches: %{customdata[0]}<br>Wins: %{customdata[1]}<br>Losses: %{customdata[2]}<extra></extra>',
    ))
    fig_venue.add_vline(x=50, line_dash='dash', line_color='#555',
                       annotation_text='50%', annotation_font_color='#555')
    fig_venue.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='#1a1a1a', tickfont=dict(color='#a0a0a0'),
                  range=[0, 100], title='Win %', title_font=dict(color='#a0a0a0')),
        yaxis=dict(showgrid=False, tickfont=dict(color='#ffffff', size=11)),
        margin=dict(l=0, r=60, t=20, b=0),
        height=500,
    )
    st.plotly_chart(fig_venue, use_container_width=True)

    # Fun facts
    significant_venues = venue_stats[venue_stats['matches'] >= 10]
    worst_venue = significant_venues.loc[significant_venues['win_pct'].idxmin()]
    # Rajiv Gandhi is SRH's home ground - always the fortress
    best_venue = venue_stats[venue_stats['venue_clean'] == 'Rajiv Gandhi Stadium'].iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-label">🏟️ Fortress</p>
            <p class="player-name">{best_venue['venue_clean']}</p>
            <p class="stat-sub">{best_venue['win_pct']}% win rate · {int(best_venue['matches'])} matches</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-label">😭 Nightmare Venue</p>
            <p class="player-name">{worst_venue['venue_clean']}</p>
            <p class="stat-sub">{worst_venue['win_pct']}% win rate · {int(worst_venue['matches'])} matches</p>
        </div>
        """, unsafe_allow_html=True)
        # ── TAB 2: BATTING ────────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-title">TOP RUN SCORERS</p>', unsafe_allow_html=True)

    # Top 10 batters for SRH
    srh_batting = srh_ball[srh_ball['team_batting'] == 2]
    batter_stats = srh_batting.groupby('batter').agg(
        runs=('batter_runs', 'sum'),
        balls=('batter_runs', 'count'),
        matches=('match_id', 'nunique'),
        fours=('batter_runs', lambda x: (x == 4).sum()),
        sixes=('batter_runs', lambda x: (x == 6).sum()),
    ).reset_index()
    batter_stats['sr'] = (batter_stats['runs'] / batter_stats['balls'] * 100).round(1)
    batter_stats['avg'] = (batter_stats['runs'] / batter_stats['matches']).round(1)
    top10 = batter_stats.sort_values('runs', ascending=False).head(10)

    # Horizontal bar chart
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=top10['batter'],
        x=top10['runs'],
        orientation='h',
        marker=dict(
            color=top10['runs'],
            colorscale=[[0, '#1a1a1a'], [1, '#F26522']],
            showscale=False,
        ),
        text=top10['runs'],
        textposition='outside',
        textfont=dict(color='#F26522', family='Rajdhani', size=13),
    ))
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='#1a1a1a', tickfont=dict(color='#a0a0a0')),
        yaxis=dict(showgrid=False, tickfont=dict(color='#ffffff', size=13), autorange='reversed'),
        margin=dict(l=0, r=60, t=20, b=0),
        height=400,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

    # ── LEGEND PLAYER COMPARISON ──
    st.markdown('<p class="section-title">LEGEND COMPARISON</p>', unsafe_allow_html=True)

    legends = {
        'DA Warner': 'David Warner',
        'S Dhawan': 'Shikhar Dhawan',
        'Abhishek Sharma': 'Abhishek Sharma',
        'TM Head': 'Travis Head',
        'KS Williamson': 'Kane Williamson',
        'H Klaasen': 'Heinrich Klaasen',
    }

    legend_stats = []
    for code, name in legends.items():
        p = srh_batting[srh_batting['batter'] == code]
        if len(p) > 0:
            runs = p['batter_runs'].sum()
            balls = len(p[p['is_wide_ball'] == False])
            matches = p['match_id'].nunique()
            sr = round(runs / balls * 100, 1) if balls > 0 else 0
            sixes = (p['batter_runs'] == 6).sum()
            legend_stats.append({
                'name': name, 'runs': runs, 'matches': matches,
                'sr': sr, 'sixes': int(sixes)
            })

    # Radar chart
    categories = ['Runs (scaled)', 'Matches', 'Strike Rate', 'Sixes']
    fig4 = go.Figure()
    colors = ['#F26522', '#FF8C42', '#FFB347', '#FFA500', '#FF6B35', '#E85D04']

    for i, p in enumerate(legend_stats):
        max_runs = max(s['runs'] for s in legend_stats)
        max_matches = max(s['matches'] for s in legend_stats)
        max_sr = max(s['sr'] for s in legend_stats)
        max_sixes = max(s['sixes'] for s in legend_stats)
        values = [
            p['runs'] / max_runs * 100,
            p['matches'] / max_matches * 100,
            p['sr'] / max_sr * 100,
            p['sixes'] / max_sixes * 100,
        ]
        fig4.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=f'rgba({int(colors[i][1:3], 16)}, {int(colors[i][3:5], 16)}, {int(colors[i][5:7], 16)}, 0.1)',
            line=dict(color=colors[i], width=2),
            name=p['name'],
        ))
    fig4.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], 
                          gridcolor='#2a2a2a', tickfont=dict(color='#555')),
            angularaxis=dict(gridcolor='#2a2a2a', 
                           tickfont=dict(color='#a0a0a0', size=12)),
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a0a0a0')),
        margin=dict(l=40, r=40, t=40, b=40),
        height=450,
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

    # ── BATTER STATS TABLE ──
    st.markdown('<p class="section-title">DETAILED STATS</p>', unsafe_allow_html=True)
    display_df = top10[['batter', 'matches', 'runs', 'balls', 'sr', 'fours', 'sixes']].copy()
    display_df.columns = ['Player', 'Matches', 'Runs', 'Balls', 'Strike Rate', 'Fours', 'Sixes']
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">RUNS vs STRIKE RATE</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#555; font-size:0.85rem; margin-bottom:1rem">Each dot = one SRH batter. Top right = best overall performer.</p>', unsafe_allow_html=True)

    # Filter batters with decent sample size
    scatter_data = batter_stats[batter_stats['balls'] >= 100].copy()

    # Highlight our legends
    legend_names = ['DA Warner', 'Abhishek Sharma', 'S Dhawan', 
                    'KS Williamson', 'H Klaasen', 'Yuvraj Singh', 'TM Head']
    scatter_data['is_legend'] = scatter_data['batter'].isin(legend_names)
    scatter_data['display_name'] = scatter_data['batter'].apply(
        lambda x: x if x in legend_names else ''
    )

    fig_scatter = go.Figure()

    # Regular players
    regular = scatter_data[~scatter_data['is_legend']]
    fig_scatter.add_trace(go.Scatter(
        x=regular['sr'],
        y=regular['runs'],
        mode='markers',
        marker=dict(size=8, color='#2a2a2a', 
                   line=dict(color='#444', width=1), opacity=0.8),
        hovertemplate='<b>%{customdata}</b><br>SR: %{x}<br>Runs: %{y}<extra></extra>',
        customdata=regular['batter'],
        name='Others',
    ))

    # Legends
    legends = scatter_data[scatter_data['is_legend']]
    fig_scatter.add_trace(go.Scatter(
        x=legends['sr'],
        y=legends['runs'],
        mode='markers+text',
        marker=dict(size=14, color='#F26522',
                   line=dict(color='#ffffff', width=2), opacity=1),
        text=legends['batter'].apply(lambda x: x.split()[-1]),
        textposition='top center',
        textfont=dict(color='#ffffff', size=11, family='Rajdhani'),
        hovertemplate='<b>%{customdata}</b><br>SR: %{x}<br>Runs: %{y}<extra></extra>',
        customdata=legends['batter'],
        name='Legends',
    ))

    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(title='Strike Rate', showgrid=True, gridcolor='#1a1a1a',
                  tickfont=dict(color='#a0a0a0'), title_font=dict(color='#a0a0a0')),
        yaxis=dict(title='Total Runs', showgrid=True, gridcolor='#1a1a1a',
                  tickfont=dict(color='#a0a0a0'), title_font=dict(color='#a0a0a0')),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a0a0a0')),
        margin=dict(l=0, r=0, t=20, b=0),
        height=400,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    # ── TAB 3: BOWLING ────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-title">TOP WICKET TAKERS</p>', unsafe_allow_html=True)

    # Top 10 bowlers for SRH
    srh_bowling = srh_ball[srh_ball['team_bowling'] == 2]
    bowler_stats = srh_bowling.groupby('bowler').agg(
        wickets=('is_wicket', 'sum'),
        runs=('total_runs', 'sum'),
        balls=('total_runs', 'count'),
        matches=('match_id', 'nunique'),
    ).reset_index()
    bowler_stats['overs'] = (bowler_stats['balls'] / 6).round(1)
    bowler_stats['economy'] = (bowler_stats['runs'] / bowler_stats['overs']).round(2)
    bowler_stats['avg'] = (bowler_stats['runs'] / bowler_stats['wickets'].replace(0, np.nan)).round(1)
    top10_bowlers = bowler_stats.sort_values('wickets', ascending=False).head(10)

    # Horizontal bar chart
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        y=top10_bowlers['bowler'],
        x=top10_bowlers['wickets'],
        orientation='h',
        marker=dict(
            color=top10_bowlers['wickets'],
            colorscale=[[0, '#1a1a1a'], [1, '#F26522']],
            showscale=False,
        ),
        text=top10_bowlers['wickets'],
        textposition='outside',
        textfont=dict(color='#F26522', family='Rajdhani', size=13),
    ))
    fig5.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='#1a1a1a', tickfont=dict(color='#a0a0a0')),
        yaxis=dict(showgrid=False, tickfont=dict(color='#ffffff', size=13), autorange='reversed'),
        margin=dict(l=0, r=60, t=20, b=0),
        height=400,
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

    # ── LEGEND BOWLER COMPARISON ──
    st.markdown('<p class="section-title">BOWLING LEGENDS</p>', unsafe_allow_html=True)

    bowling_legends = {
    'B Kumar': 'Bhuvneshwar Kumar',
    'Rashid Khan': 'Rashid Khan',
    'DW Steyn': 'Dale Steyn',
    'T Natarajan': 'T Natarajan',
    'PJ Cummins': 'Pat Cummins',
}

    cols = st.columns(5)
    for i, (code, name) in enumerate(bowling_legends.items()):
        p = srh_bowling[srh_bowling['bowler'] == code]
        if len(p) > 0:
            wickets = int(p['is_wicket'].sum())
            runs = int(p['total_runs'].sum())
            balls = len(p)
            overs = balls / 6
            economy = round(runs / overs, 2) if overs > 0 else 0
            matches = p['match_id'].nunique()
            with cols[i]:
                st.markdown(f"""
                <div class="player-card">
                    <p class="player-role">🎯 Bowler</p>
                    <p class="player-name">{name.upper()}</p>
                    <p class="player-stat">{wickets}</p>
                    <p class="player-stat-label">Wickets</p>
                    <br>
                    <p class="stat-sub">Economy: {economy}</p>
                    <p class="stat-sub">Matches: {matches}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

    # ── ECONOMY COMPARISON ──
    st.markdown('<p class="section-title">ECONOMY RATE COMPARISON</p>', unsafe_allow_html=True)

    legend_bowl_stats = []
    for code, name in bowling_legends.items():
        p = srh_bowling[srh_bowling['bowler'] == code]
        if len(p) > 0:
            wickets = int(p['is_wicket'].sum())
            runs = int(p['total_runs'].sum())
            balls = len(p)
            overs = balls / 6
            economy = round(runs / overs, 2) if overs > 0 else 0
            legend_bowl_stats.append({'name': name, 'wickets': wickets, 'economy': economy})

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=[p['economy'] for p in legend_bowl_stats],
        y=[p['wickets'] for p in legend_bowl_stats],
        mode='markers+text',
        marker=dict(
            size=20,
            color='#F26522',
            line=dict(color='#ffffff', width=2),
            opacity=0.9,
        ),
        text=[p['name'].split()[-1] for p in legend_bowl_stats],
        textposition='top center',
        textfont=dict(color='#ffffff', size=11, family='Rajdhani'),
    ))
    fig6.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0a0a0', family='Inter'),
        xaxis=dict(title='Economy Rate', showgrid=True, gridcolor='#1a1a1a',
                  tickfont=dict(color='#a0a0a0'), title_font=dict(color='#a0a0a0')),
        yaxis=dict(title='Wickets', showgrid=True, gridcolor='#1a1a1a',
                  tickfont=dict(color='#a0a0a0'), title_font=dict(color='#a0a0a0')),
        margin=dict(l=0, r=0, t=20, b=0),
        height=350,
    )
    st.plotly_chart(fig6, use_container_width=True)

    # ── DETAILED STATS TABLE ──
    st.markdown('<p class="section-title">DETAILED STATS</p>', unsafe_allow_html=True)
    display_bowl = top10_bowlers[['bowler', 'matches', 'wickets', 'runs', 'overs', 'economy']].copy()
    display_bowl.columns = ['Player', 'Matches', 'Wickets', 'Runs', 'Overs', 'Economy']
    st.dataframe(display_bowl, use_container_width=True, hide_index=True)
    # ── TAB 4: PLAYER SPOTLIGHT ───────────────────────────────────
with tab4:
    st.markdown('<p class="section-title">SRH ALL TIME XI</p>', unsafe_allow_html=True)

    field_html = """<div style="background:linear-gradient(135deg,#0a1a0a,#0f2a0f);border:1px solid rgba(242,101,34,0.3);border-radius:16px;padding:2rem;margin-bottom:2rem;text-align:center">
    <p style="font-family:Rajdhani;color:#F26522;letter-spacing:3px;font-size:0.8rem;margin-bottom:1.5rem">⚡ ALL TIME PLAYING XI</p>
    <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1.5rem">
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">DW</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Warner</p><p style="color:#F26522;font-size:0.65rem">C · OPENER</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">AS</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Abhishek</p><p style="color:#F26522;font-size:0.65rem">OPENER</p></div>
    </div>
    <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1.5rem">
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">SD</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Dhawan</p><p style="color:#F26522;font-size:0.65rem">#3</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">KW</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Kane</p><p style="color:#F26522;font-size:0.65rem">VC · KANE MAMA</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">HK</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Klaasen</p><p style="color:#F26522;font-size:0.65rem">#5</p></div>
    </div>
    <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1.5rem">
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">YS</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Yuvraj</p><p style="color:#F26522;font-size:0.65rem">#6</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">PC</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Cummins</p><p style="color:#F26522;font-size:0.65rem">#7</p></div>
    </div>
    <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:1rem">
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">RK</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Rashid</p><p style="color:#F26522;font-size:0.65rem">SPINNER</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">BK</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Bhuvi</p><p style="color:#F26522;font-size:0.65rem">SWING KING</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">TN</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Natarajan</p><p style="color:#F26522;font-size:0.65rem">DEATH BOWLER</p></div>
    <div><div style="background:#1a1a1a;border:2px solid #F26522;color:#F26522;border-radius:50%;width:55px;height:55px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1rem;font-weight:700">SS</div><p style="color:#fff;font-size:0.75rem;margin-top:0.4rem;font-weight:600">Sandeep</p><p style="color:#F26522;font-size:0.65rem">PACER</p></div>
    </div>
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(242,101,34,0.2)">
    <p style="font-family:Rajdhani;color:#555;font-size:0.75rem;letter-spacing:2px">🧡 HONORARY MENTION — BCJ CUTTING · 2016 FINAL HERO</p>
    </div></div>"""
    st.markdown(field_html, unsafe_allow_html=True)

    st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)

    # ── PLAYER STAT CARDS ──
    st.markdown('<p class="section-title">PLAYER CARDS</p>', unsafe_allow_html=True)

    all_players = {
        'DA Warner': {'name': 'David Warner', 'role': 'C .Opener 🇦🇺', 'type': 'batter'},
        'Abhishek Sharma': {'name': 'Abhishek Sharma', 'role': 'Opener 🇮🇳', 'type': 'batter'},
        'S Dhawan': {'name': 'Shikhar Dhawan', 'role': 'Top Order 🇮🇳', 'type': 'batter'},
        'KS Williamson': {'name': 'Kane Williamson', 'role': 'VC .Kane Mama 🇳🇿', 'type': 'batter'},
        'H Klaasen': {'name': 'Heinrich Klaasen', 'role': 'Middle Order 🇿🇦', 'type': 'batter'},
        'Yuvraj Singh': {'name': 'Yuvraj Singh', 'role': 'Power Hitter 🇮🇳', 'type': 'batter'},
        'PJ Cummins': {'name': 'Pat Cummins', 'role': 'Pacer 🇦🇺', 'type': 'bowler'},
        'Rashid Khan': {'name': 'Rashid Khan', 'role': 'Spin Ace 🇦🇫', 'type': 'bowler'},
        'B Kumar': {'name': 'Bhuvneshwar Kumar', 'role': 'Swing King 🇮🇳', 'type': 'bowler'},
        'T Natarajan': {'name': 'T Natarajan', 'role': 'Death Specialist 🇮🇳', 'type': 'bowler'},
        'Sandeep Sharma': {'name': 'Sandeep Sharma', 'role': 'Support Pacer 🇮🇳', 'type': 'bowler'},
    }

    srh_batting = srh_ball[srh_ball['team_batting'] == 2]
    srh_bowling = srh_ball[srh_ball['team_bowling'] == 2]

    cols = st.columns(3)
    for i, (code, info) in enumerate(all_players.items()):
        with cols[i % 3]:
            if info['type'] == 'batter':
                p = srh_batting[srh_batting['batter'] == code]
                runs = int(p['batter_runs'].sum())
                balls = len(p[p['is_wide_ball'] == False])
                matches = p['match_id'].nunique()
                sr = round(runs / balls * 100, 1) if balls > 0 else 0
                sixes = int((p['batter_runs'] == 6).sum())
                st.markdown(f"""
                <div class="player-card" style="margin-bottom: 1rem;">
                    <p class="player-role">{info['role']}</p>
                    <p class="player-name">{info['name'].upper()}</p>
                    <p class="player-stat">{runs}</p>
                    <p class="player-stat-label">Runs</p>
                    <div style="display:flex; justify-content:space-around; margin-top:1rem;">
                        <div>
                            <p style="color:#F26522; font-family:'Bebas Neue'; font-size:1.3rem; margin:0">{sr}</p>
                            <p style="color:#555; font-size:0.65rem; letter-spacing:1px;">SR</p>
                        </div>
                        <div>
                            <p style="color:#F26522; font-family:'Bebas Neue'; font-size:1.3rem; margin:0">{matches}</p>
                            <p style="color:#555; font-size:0.65rem; letter-spacing:1px;">MATCHES</p>
                        </div>
                        <div>
                            <p style="color:#F26522; font-family:'Bebas Neue'; font-size:1.3rem; margin:0">{sixes}</p>
                            <p style="color:#555; font-size:0.65rem; letter-spacing:1px;">SIXES</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                p = srh_bowling[srh_bowling['bowler'] == code]
                wickets = int(p['is_wicket'].sum())
                runs = int(p['total_runs'].sum())
                balls = len(p)
                overs = balls / 6
                economy = round(runs / overs, 2) if overs > 0 else 0
                matches = p['match_id'].nunique()
                st.markdown(f"""
                <div class="player-card" style="margin-bottom: 1rem;">
                    <p class="player-role">{info['role']}</p>
                    <p class="player-name">{info['name'].upper()}</p>
                    <p class="player-stat">{wickets}</p>
                    <p class="player-stat-label">Wickets</p>
                    <div style="display:flex; justify-content:space-around; margin-top:1rem;">
                        <div>
                            <p style="color:#F26522; font-family:'Bebas Neue'; font-size:1.3rem; margin:0">{economy}</p>
                            <p style="color:#555; font-size:0.65rem; letter-spacing:1px;">ECONOMY</p>
                        </div>
                        <div>
                            <p style="color:#F26522; font-family:'Bebas Neue'; font-size:1.3rem; margin:0">{matches}</p>
                            <p style="color:#555; font-size:0.65rem; letter-spacing:1px;">MATCHES</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="srh-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">PERFORMANCE BY VENUE</p>', unsafe_allow_html=True)

    