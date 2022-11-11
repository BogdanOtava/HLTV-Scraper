from url_shortener import shorten_url
from bs4 import BeautifulSoup
from config import DATA
import pandas as pd
import requests
import os

def get_news(year:int, month:str) -> pd.DataFrame:
    """
    Returns a CSV file that contains the date when the article was posted, the title, and a link to it, for the year and month given as parameters.

    Parameters:
        - year (int): the year when the news were posted.
        - month (str): the month when the news were posted.
    """

    try:
        source = requests.get(f"https://www.hltv.org/news/archive/{year}/{month}").text
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    soup = BeautifulSoup(source, "lxml")

    news = soup.find("div", class_="standard-box standard-list")

    attributes = []
    columns = ["date", "title", "link"]

    for article in news.find_all("a", href=True):

        title = article.find("div", class_="newstext").text
        date = article.find("div", class_="newsrecent").text
        link = article["href"]

        # shorten url and add the website name and domain because the 'href' attribute doesn't include it
        short_link = shorten_url(f"hltv.org{link}")

        # append a list of the scraped data to the 'attributes' list
        attributes.append([date, title, short_link])

    # create a new dataframe out of the scraped data and then export it as a CSV file
    data = pd.DataFrame(attributes, columns=columns)

    if not os.path.isdir(f"{DATA}/news"):
        os.makedirs(f"{DATA}/news")

    data.to_csv(f"{DATA}/news/{year}_{month}.csv", index=False)
