import pandas as pd
import requests

def get_statistics(start_date:str = "all", end_date:str = None, match_type:str = None, maps:list = None, team:str = None) -> pd.DataFrame:
    """
    Returns a CSV file that contains the stats of players for the given filters.

    Parameters:
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
        source = requests.get("https://www.hltv.org/stats/players?", params=payload)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    print(source.url)