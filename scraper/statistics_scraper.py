from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_statistics(top:int = 10, start_date:str = "all", end_date:str = None, match_type:str = None, maps:list = None, team:str = None) -> pd.DataFrame:
    """
    Returns a CSV file that contains the stats of players for the given filters, based on the rating of the players.

    Parameters:
        - top (int): how many players to go down the leaderboard. Default is 10.
        - start_date (str): start point of the information. This needs to be passed as a string as: '2022-10-15' or any other date with the format 'year-month-day'. It's defaulted at 'all' which returns stats from '2012-01-01' to present day.
        - end_date (str): end point of the information. This should be used together with the 'start_date' parameter to get information in a specific period of time, e.g. a calendaristic year. Needs to be passed as a string as: '2022-10-15' or any other date with the format 'year-month-day'.
        - match_type (str): the environment where the match was played. Allowed options: LAN, Online, BigEvents, Majors.
        - maps (list): the map(s) played. Needs to be passed a a list with the maps as strings. Default is 'all' which includes all maps that are or were in the competitive pool. E.g. de_dust2, de_mirage, etc.
        - team (str): refers to the two sides. Needs to be passed as either 'COUNTER_TERRORIST' or 'TERRORIST'. The default is set to both sides.
    """

    payload = {
        "start_date": start_date,
        "end_date": end_date,
        "match_type": match_type,
        "maps": maps,
        "team": team
    }

    try:
        source = requests.get("https://www.hltv.org/stats/players?", params=payload).text
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    soup = BeautifulSoup(source, "lxml")

    attributes = []
    columns = ["player", "maps_played", "rounds_played", "kd_difference", "kd_ratio", "rating"]
    count = 0

    table = soup.find("tbody")

    for attribute in table.find_all("tr"):

        player = attribute.find("a").text
        kd_difference = attribute.find("td", class_="kdDiffCol").text
        rating = attribute.find("td", class_="ratingCol").text
        items = [i.get_text() for i in attribute.find_all("td", class_="statsDetail")]

        attributes.append([player, items[0], items[1], kd_difference, items[2], rating])

        top -= 1

        if top == 0:
            break

    print(attributes)