from url_shortener import shorten_url
from bs4 import BeautifulSoup
from config import DATA
from logger import logger
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

    news = soup.find_all("a", class_="newsline article", href=True)

    attributes = []
    columns = ["date", "title", "link"]
    count = 0

    for article in news:

        title = article.find("div", class_="newstext").text
        date = article.find("div", class_="newsrecent").text
        link = article["href"]

        # shorten url and add the website name and domain because the 'href' attribute doesn't include it
        short_link = shorten_url(f"hltv.org{link}")

        # append a list of the scraped data to the 'attributes' list
        attributes.append([date, title, short_link])

        count += 1
        logger.debug(f"Article(s) scraped: {count}...")

    logger.info(f"Successfully scraped {count} articles from {month} {year}.")

    # create a new dataframe out of the scraped data and then export it as a CSV file
    data = pd.DataFrame(attributes, columns=columns)

    if not os.path.isdir(f"{DATA}/news"):
        os.makedirs(f"{DATA}/news")

    data.to_csv(f"{DATA}/news/{year}_{month}.csv", index=False)

    logger.info(f"Scraped data was exported in 'data/news/{year}_{month}.csv'.")
