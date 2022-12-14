from bs4 import BeautifulSoup
from config import *
from logger import logger
import pandas as pd
import requests
import time
import os

def get_team_rankings(year:int, month:str, day:int) -> pd.DataFrame:
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

    rankings = soup.find_all("div", class_="ranked-team standard-box")

    attributes = []
    columns = ["rank", "team_name", "points", "players"]
    count = 0

    for team in rankings:

        try:
            team_ranking = team.find("span", class_="position").text.replace("#", "")
            team_name = team.find("span", class_="name").text
            team_points = team.find("span", class_="points").text

            # list of all 5 players for each team
            players = [player.get_text() for player in team.find_all("div", class_="rankingNicknames")]

        except BaseException:
            logger.error("Could not scrape a teams data...")

        else:
            # appends a list of the scraped data to the 'attributes' list
            attributes.append([team_ranking, team_name, team_points, players])

            count += 1
            logger.debug(f"Teams scraped: {count}...")
            time.sleep(TIME)

    logger.info(f"Successfully scraped the HLTV World Rankings from {day}-{month}-{year}.")

    # create a new dataframe out of the scraped data and then export it as a CSV file
    data = pd.DataFrame(attributes, columns=columns)

    if not os.path.exists(f"{DATA}/team_rankings"):
        os.makedirs(f"{DATA}/team_rankings")

    data.to_csv(f"{DATA}/team_rankings/{year}_{month}_{day}.csv", index=False)

    logger.info(f"Scraped data was exported in 'data/team_rankings/{year}_{month}_{day}.csv'.")
