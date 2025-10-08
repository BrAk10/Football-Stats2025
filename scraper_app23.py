import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Comment
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

LEAGUE_CONFIGS = [
    ("Premier League",
     ["stats_standard_9", "stats_keeper_9", "stats_shooting_9",
      "stats_passing_9", "stats_defense_9", "stats_possession_9"],
     [
         ("Liverpool", "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats"),
         ("Arsenal", "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats"),
         ("Crystal Palace", "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats"),
         ("Tottenham", "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats"),
         ("Sunderland", "https://fbref.com/en/squads/8ef52968/Sunderland-Stats"),
         ("Bournemouth", "https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats"),
         ("Manchester City", "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"),
         ("Chelsea", "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats"),
         ("Everton", "https://fbref.com/en/squads/d3fd31cc/Everton-Stats"),
         ("Brighton", "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats"),
         ("Fulham", "https://fbref.com/en/squads/fd962109/Fulham-Stats"),
         ("Leeds", "https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats"),
         ("Brentford", "https://fbref.com/en/squads/cd051869/Brentford-Stats"),
         ("Manchester United", "https://fbref.com/en/squads/19538871/Manchester-United-Stats"),
         ("Newcastle United", "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats"),
         ("Aston Villa", "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats"),
         ("Nottingham Forest", "https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats"),
         ("Burnley", "https://fbref.com/en/squads/943e8050/Burnley-Stats"),
         ("West Ham United", "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats"),
         ("Wolves", "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats"),
     ]),
    ("La Liga",
     ["stats_standard_12", "stats_keeper_12", "stats_shooting_12",
      "stats_passing_12", "stats_defense_12", "stats_possession_12"],
     [
         ("Barcelona", "https://fbref.com/en/squads/206d90db/Barcelona-Stats"),
         ("Real Madrid", "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"),
         ("Villarreal", "https://fbref.com/en/squads/2a8183b3/Villarreal-Stats"),
         ("Elche", "https://fbref.com/en/squads/6c8b07df/Elche-Stats"),
         ("Atletico Madrid", "https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats"),
         ("Real Betis", "https://fbref.com/en/squads/fc536746/Real-Betis-Stats"),
         ("Espanyol", "https://fbref.com/en/squads/a8661628/Espanyol-Stats"),
         ("Getafe", "https://fbref.com/en/squads/7848bd64/Getafe-Stats"),
         ("Sevilla", "https://fbref.com/en/squads/ad2be733/Sevilla-Stats"),
         ("Athletic Club", "https://fbref.com/en/squads/2b390eca/Athletic-Club-Stats"),
         ("Alaves", "https://fbref.com/en/squads/8d6fd021/Alaves-Stats"),
         ("Valencia", "https://fbref.com/en/squads/dcc91a7b/Valencia-Stats"),
         ("Osasuna", "https://fbref.com/en/squads/03c57e2b/Osasuna-Stats"),
         ("Oviedo", "https://fbref.com/en/squads/ab358912/Oviedo-Stats"),
         ("Levante", "https://fbref.com/en/squads/9800b6a1/Levante-Stats"),
         ("Rayo Vallecano", "https://fbref.com/en/squads/98e8af82/Rayo-Vallecano-Stats"),
         ("Celta Vigo", "https://fbref.com/en/squads/f25da7fb/Celta-Vigo-Stats"),
         ("Real Sociedad", "https://fbref.com/en/squads/e31d1cd9/Real-Sociedad-Stats"),
         ("Mallorca", "https://fbref.com/en/squads/2aa12281/Mallorca-Stats"),
         ("Girona", "https://fbref.com/en/squads/9024a00a/Girona-Stats"),
     ]),
    ("Ligue 1",
     ["stats_standard_13", "stats_keeper_13", "stats_shooting_13",
      "stats_passing_13", "stats_defense_13", "stats_possession_13"],
     [
         ("Paris SG", "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats"),
         ("Lyon", "https://fbref.com/en/squads/d53c0b06/Lyon-Stats"),
         ("Marseille", "https://fbref.com/en/squads/5725cc7b/Marseille-Stats"),
         ("Monaco", "https://fbref.com/en/squads/fd6114db/Monaco-Stats"),
         ("Strasbourg", "https://fbref.com/en/squads/c0d3eab4/Strasbourg-Stats"),
         ("Lille", "https://fbref.com/en/squads/cb188c0c/Lille-Stats"),
         ("Lens", "https://fbref.com/en/squads/fd4e0f7d/Lens-Stats"),
         ("Rennes", "https://fbref.com/en/squads/b3072e00/Rennes-Stats"),
         ("Brest", "https://fbref.com/en/squads/fb08dbb3/Brest-Stats"),
         ("Toulouse", "https://fbref.com/en/squads/3f8c4b5f/Toulouse-Stats"),
         ("Paris FC", "https://fbref.com/en/squads/056a5a75/Paris-FC-Stats"),
         ("Nice", "https://fbref.com/en/squads/132ebc33/Nice-Stats"),
         ("Lorient", "https://fbref.com/en/squads/d2c87802/Lorient-Stats"),
         ("Auxerre", "https://fbref.com/en/squads/5ae09109/Auxerre-Stats"),
         ("Le Havre", "https://fbref.com/en/squads/5c2737db/Le-Havre-Stats"),
         ("Nantes", "https://fbref.com/en/squads/d7a486cd/Nantes-Stats"),
         ("Angers", "https://fbref.com/en/squads/69236f98/Angers-Stats"),
         ("Metz", "https://fbref.com/en/squads/f83960ae/Metz-Stats"),
     ]),
    ("Bundesliga",
     ["stats_standard_20", "stats_keeper_20", "stats_shooting_20",
      "stats_passing_20", "stats_defense_20", "stats_possession_20"],
     [
         ("Bayern Munich", "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats"),
         ("Dortmund", "https://fbref.com/en/squads/add600ae/Dortmund-Stats"),
         ("RB Leipzig", "https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats"),
         ("Eintracht Frankfurt", "https://fbref.com/en/squads/f0ac8ee6/Eintracht-Frankfurt-Stats"),
         ("Stuttgart", "https://fbref.com/en/squads/598bc722/Stuttgart-Stats"),
         ("Bayer Leverkusen", "https://fbref.com/en/squads/c7a9f859/Bayer-Leverkusen-Stats"),
         ("Koln", "https://fbref.com/en/squads/bc357bf7/Koln-Stats"),
         ("Freiburg", "https://fbref.com/en/squads/a486e511/Freiburg-Stats"),
         ("St Pauli", "https://fbref.com/en/squads/54864664/St-Pauli-Stats"),
         ("Hoffenheim", "https://fbref.com/en/squads/033ea6b8/Hoffenheim-Stats"),
         ("Union Berlin", "https://fbref.com/en/squads/7a41008f/Union-Berlin-Stats"),
         ("Wolfsburg", "https://fbref.com/en/squads/4eaa11d7/Wolfsburg-Stats"),
         ("Hamburger SV", "https://fbref.com/en/squads/26790c6a/Hamburger-SV-Stats"),
         ("Mainz 05", "https://fbref.com/en/squads/a224b06a/Mainz-05-Stats"),
         ("Werder Bremen", "https://fbref.com/en/squads/62add3bf/Werder-Bremen-Stats"),
         ("Augsburg", "https://fbref.com/en/squads/0cdc4311/Augsburg-Stats"),
         ("Heidenheim", "https://fbref.com/en/squads/18d9d2a7/Heidenheim-Stats"),
         ("Monchengladbach", "https://fbref.com/en/squads/32f3ee20/Monchengladbach-Stats"),
     ]),
    ("Serie A",
     ["stats_standard_11", "stats_keeper_11", "stats_shooting_11",
      "stats_passing_11", "stats_defense_11", "stats_possession_11"],
     [
         ("Milan", "https://fbref.com/en/squads/dc56fe14/Milan-Stats"),
         ("Napoli", "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats"),
         ("Roma", "https://fbref.com/en/squads/cf74a709/Roma-Stats"),
         ("Juventus", "https://fbref.com/en/squads/e0652b02/Juventus-Stats"),
         ("Inter", "https://fbref.com/en/squads/d609edc0/Internazionale-Stats"),
         ("Atalanta", "https://fbref.com/en/squads/922493f3/Atalanta-Stats"),
         ("Cremonese", "https://fbref.com/en/squads/9aad3a77/Cremonese-Stats"),
         ("Como", "https://fbref.com/en/squads/28c9c3cd/Como-Stats"),
         ("Cagliari", "https://fbref.com/en/squads/c4260e09/Cagliari-Stats"),
         ("Bologna", "https://fbref.com/en/squads/1d8099f8/Bologna-Stats"),
         ("Udinese", "https://fbref.com/en/squads/04eea015/Udinese-Stats"),
         ("Lazio", "https://fbref.com/en/squads/7213da33/Lazio-Stats"),
         ("Sassuolo", "https://fbref.com/en/squads/e2befd26/Sassuolo-Stats"),
         ("Parma", "https://fbref.com/en/squads/eab4234c/Parma-Stats"),
         ("Torino", "https://fbref.com/en/squads/105360fe/Torino-Stats"),
         ("Fiorentina", "https://fbref.com/en/squads/421387cf/Fiorentina-Stats"),
         ("Hellas Verona", "https://fbref.com/en/squads/0e72edf2/Hellas-Verona-Stats"),
         ("Pisa", "https://fbref.com/en/squads/4cceedfc/Pisa-Stats"),
         ("Genoa", "https://fbref.com/en/squads/658bf2de/Genoa-Stats"),
         ("Lecce", "https://fbref.com/en/squads/ffcbe334/Lecce-Stats"),
     ]),
]

TABLE_ID_NAME_MAP = {
    "stats_standard_9": "standard_stats",
    "stats_keeper_9": "keeper_stats",
    "stats_shooting_9": "shooting_stats",
    "stats_passing_9": "passing_stats",
    "stats_defense_9": "defense_stats",
    "stats_possession_9": "possession_stats",
    "stats_standard_12": "standard_stats",
    "stats_keeper_12": "keeper_stats",
    "stats_shooting_12": "shooting_stats",
    "stats_passing_12": "passing_stats",
    "stats_defense_12": "defense_stats",
    "stats_possession_12": "possession_stats",
    "stats_standard_13": "standard_stats",
    "stats_keeper_13": "keeper_stats",
    "stats_shooting_13": "shooting_stats",
    "stats_passing_13": "passing_stats",
    "stats_defense_13": "defense_stats",
    "stats_possession_13": "possession_stats",
    "stats_standard_20": "standard_stats",
    "stats_keeper_20": "keeper_stats",
    "stats_shooting_20": "shooting_stats",
    "stats_passing_20": "passing_stats",
    "stats_defense_20": "defense_stats",
    "stats_possession_20": "possession_stats",
    "stats_standard_11": "standard_stats",
    "stats_keeper_11": "keeper_stats",
    "stats_shooting_11": "shooting_stats",
    "stats_passing_11": "passing_stats",
    "stats_defense_11": "defense_stats",
    "stats_possession_11": "possession_stats",
}

def extract_table_from_comment(soup, table_id):
    div_id = "div_" + table_id
    div = soup.find("div", id=div_id)
    if div:
        comment = div.find_all(string=lambda text: isinstance(text, Comment))
        for c in comment:
            comment_soup = BeautifulSoup(c, "html.parser")
            table = comment_soup.find("table", id=table_id)
            if table:
                return table
    return None

def scrape_team_tables(team_name, url, table_ids):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    team_tables = {}
    for table_id in table_ids:
        table = soup.find("table", id=table_id)
        if not table:
            table = extract_table_from_comment(soup, table_id)
        if not table:
            st.warning(f"Table {table_id} not found for {team_name} at {url}")
            continue
        headers = [th.get("data-stat") for th in table.find("thead").find_all("th", scope="col")]
        rows = []
        for tr in table.find("tbody").find_all("tr"):
            cells = [td.text.strip() for td in tr.find_all(["td", "th"])]
            if len(cells) == len(headers):
                row = dict(zip(headers, cells))
                row["Team"] = team_name
                rows.append(row)
        df = pd.DataFrame(rows)
        friendly_name = TABLE_ID_NAME_MAP.get(table_id, table_id)
        team_tables[friendly_name] = df
    return team_tables

def convert_numeric_columns(df):
    for col in df.columns:
        if col.lower() not in ['player', 'team', 'pos', 'position']:
            df[col] = pd.to_numeric(df[col].str.replace(',', '', regex=False).replace('', '0'), errors='coerce').fillna(0)
    return df

def plot_top_scoring_players(df):
    if 'player' in df.columns and 'goals' in df.columns:
        data = df.groupby('player')['goals'].sum().reset_index().sort_values('goals', ascending=False).head(10)
        fig = px.bar(data, x='player', y='goals', title='Top 10 Goal Scorers', text='goals')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

def plot_top_tackles(df):
    if 'player' in df.columns and 'tackles_won' in df.columns:
        data = df.groupby('player')['tackles_won'].sum().reset_index().sort_values('tackles_won', ascending=False).head(10)
        fig = px.bar(data, x='player', y='tackles_won', title='Top 10 Tackles', text='tackles_won', color='tackles_won')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

def plot_progressive_passing(df):
    if 'player' in df.columns and 'progressive_passes' in df.columns:
        data = df.groupby('player')['progressive_passes'].sum().reset_index().sort_values('progressive_passes', ascending=False).head(10)
        fig = px.bar(data, x='player', y='progressive_passes', title='Top 10 Progressive Passers', text='progressive_passes', color='progressive_passes')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

def plot_progressive_carries(df):
    if 'player' in df.columns and 'progressive_carries' in df.columns:
        data = df.groupby('player')['progressive_carries'].sum().reset_index().sort_values('progressive_carries', ascending=False).head(10)
        fig = px.bar(data, x='player', y='progressive_carries', title='Top 10 Progressive Carries', text='progressive_carries', color='progressive_carries')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

def plot_goalkeeper_saves(df):
    if 'player' in df.columns:
        candidates = ['gk_saves', 'gk_shots_on_target_against']
        col = next((c for c in candidates if c in df.columns), None)
        if col:
            data = df.groupby('player')[col].sum().reset_index()
            data = data.sort_values(col, ascending=False).head(10)
            fig = px.bar(data, x='player', y=col, title='Top 10 Goalkeeper Saves', text=col)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig)

def plot_player_radar_combined(player_stats, player_name):
    keys = [
        'goals', 'assists', 'shots', 'touches_att_3rd', 'progressive_carries', 'tackles_won', 'interceptions'
    ]
    values = [float(player_stats[k]) if k in player_stats else 0 for k in keys]
    max_value = max(values) if values else 1
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=keys, fill='toself', name=player_name))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max_value * 1.1])),
        showlegend=False,
        title=f'{player_name} Performance Radar'
    )
    st.plotly_chart(fig)

st.title("Full Football Stats Dashboard with All Teams and Visuals")

# Step 1: League selection
selected_leagues = st.multiselect("Select Leagues", [league[0] for league in LEAGUE_CONFIGS])

league_team_selection = {}
if selected_leagues:
    # Step 2: Team selection for each selected league
    for league_name in selected_leagues:
        league = next(l for l in LEAGUE_CONFIGS if l[0] == league_name)
        all_team_names = [t[0] for t in league[2]]
        selected_teams = st.multiselect(f"Select Teams for {league_name}", all_team_names, key=f"{league_name}_teams")
        league_team_selection[league_name] = [t for t in league[2] if t[0] in selected_teams]

# Step 3: Stat category selection (only if some teams chosen)
selected_stats = []
if any(league_team_selection.values()):
    DISPLAY_OPTIONS = [
        "standard_stats", "passing_stats", "defense_stats", "keeper_stats",
        "possession_stats", "shooting_stats"
    ]
    LABELS = {
        "standard_stats": "Standard Stats",
        "passing_stats": "Passing Stats",
        "defense_stats": "Defense Stats",
        "keeper_stats": "Keeper Stats",
        "possession_stats": "Possession Stats",
        "shooting_stats": "Shooting Stats"
    }
    selected_stats = st.multiselect(
        "Select stat categories to display",
        options=DISPLAY_OPTIONS,
        format_func=lambda x: LABELS.get(x, x),
        default=["standard_stats"]
    )

# Step 4: Enable Run Scraping button only if all selections made
scraping_enabled = (
    bool(selected_leagues) and
    any(league_team_selection.values()) and
    bool(selected_stats)
)

if scraping_enabled:
    if st.button("Run Scraping"):
        all_data = {k: [] for k in TABLE_ID_NAME_MAP.values()}
        for league_name, teams in league_team_selection.items():
            table_ids = next(league[1] for league in LEAGUE_CONFIGS if league[0] == league_name)
            for team_name, url in teams:
                st.info(f"Scraping {team_name} ({league_name})...")
                team_tables = scrape_team_tables(team_name, url, table_ids)
                for key, df in team_tables.items():
                    if key in all_data:
                        all_data[key].append(df)
        merged_data = {}
        for key, list_dfs in all_data.items():
            if list_dfs:
                df_concat = pd.concat(list_dfs, ignore_index=True)
                df_concat = convert_numeric_columns(df_concat)
                merged_data[key] = df_concat
        st.session_state['data'] = merged_data
else:
    st.info("Please select at least one league, team, and stat category before running scraping.")

# Display results and visualizations if data exists
if 'data' in st.session_state:
    data = st.session_state['data']

    # Define players variable safely
    if 'standard_stats' in data and 'player' in data['standard_stats'].columns:
        players = data['standard_stats']['player'].unique()
    else:
        players = []

    for stat in selected_stats:
        if stat in data and not data[stat].empty:
            st.subheader(LABELS.get(stat, stat))
            st.dataframe(data[stat])

            if stat == "standard_stats":
                plot_top_scoring_players(data[stat])
            elif stat == "defense_stats":
                plot_top_tackles(data[stat])
            elif stat == "passing_stats":
                plot_progressive_passing(data[stat])
            elif stat == "possession_stats":
                plot_progressive_carries(data[stat])
            elif stat == "keeper_stats":
                plot_goalkeeper_saves(data[stat])

    if players.size > 0:
        # New UI: Multi-select players for individual radars
        selected_players = st.multiselect("Select Players for Individual Radars", players, default=players[:2], key="individual_radar")

        if selected_players:
            keys = ['goals', 'assists', 'shots', 'touches_att_3rd', 'progressive_carries', 'tackles_won', 'interceptions']

            for player in selected_players:
                player_data_frames = []
                for cat in ['standard_stats', 'passing_stats', 'defense_stats', 'shooting_stats', 'possession_stats', 'keeper_stats']:
                    if cat in data and not data[cat].empty:
                        player_df = data[cat][data[cat]['player'] == player]
                        if not player_df.empty:
                            player_data_frames.append(player_df.iloc[0])
                if player_data_frames:
                    combined_series = pd.concat(player_data_frames, axis=0)
                    combined_series = combined_series[~combined_series.index.duplicated(keep='first')]
                    plot_player_radar_combined(combined_series, player)

    if 'standard_stats' in data:
        st.download_button(
            "Download Standard Stats CSV",
            data['standard_stats'].to_csv(index=False),
            file_name="standard_stats.csv"
        )