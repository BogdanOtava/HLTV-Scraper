from scraper.rankings_scraper import get_rankings
from scraper.news_scraper import get_news
from scraper.statistics_scraper import get_statistics

if __name__ == "__main__":
    get_rankings(2022, "november", 14)
    get_news(2022, "october")
    get_statistics()