from scraper.rankings_scraper import get_rankings
from scraper.news_scraper import get_news

if __name__ == "__main__":
    get_rankings(2022, "february", 8)
    get_news(2022, "november")