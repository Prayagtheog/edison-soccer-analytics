from fastapi import FastAPI
from scraper import scrape_all_data
import pandas as pd

app = FastAPI()

# Load data once at startup
@app.on_event("startup")
async def load_data():
    global team_data
    team_data = scrape_all_data()

# Functions Claude can call
@app.get("/api/player/{name}")
def get_player_stats(name: str):
    # Return stats for specific player
    pass

@app.get("/api/team/top_scorers")
def get_top_scorers(limit: int = 5):
    # Return top goal scorers
    pass

@app.get("/api/opponent/{team_name}")
def get_opponent_info(team_name: str):
    # Find games vs this team, get their record
    pass
