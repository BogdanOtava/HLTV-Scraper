from bs4 import BeautifulSoup
from config import DATA
import pandas as pd
import requests
import os

def get_rankings(year:int, month:str, day:int):
    """
    Returns a CSV file with the CS:GO World Rankings (rank, team name, points, players) according to HLTV for the given date. The rankings come out a few times a month, so it needs to be an exact date when the rankings were posted. The dates can be taken from the 'rankings' tab of the website.

    Parameters:
        - year (int): the year when the rankings were posted.
        - month (str): the month when the rankings were posted.
        - day (int): the day when the rankings were posted.
    """

    try:
        source = requests.get(f"https://www.hltv.org/ranking/teams/{year}/{month}/{day}").text
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    soup = BeautifulSoup(source, "lxml")

    world_ranking = soup.find("div", class_="ranking")

    attributes = []
    columns = ["rank", "team_name", "points", "players"]

    for team in world_ranking.find_all("div", class_="ranked-team standard-box"):

        team_ranking = team.find("span", class_="position").text.replace("#", "")
        team_name = team.find("span", class_="name").text
        team_points = team.find("span", class_="points").text

        players = []

        for player in team.find_all("div", class_="rankingNicknames"):
            players.append(player.get_text())

        # appends a list of the scraped data to the 'attributes' list
        attributes.append([team_ranking, team_name, team_points, players])

    # create a new dataframe out of the scraped data and then export it as a CSV file
    data = pd.DataFrame(attributes, columns=columns)

    if not os.path.exists(f"{DATA}/rankings"):
        os.makedirs(f"{DATA}/rankings")

    data.to_csv(f"{DATA}/rankings/{year}_{month}_{day}.csv", index=False)
