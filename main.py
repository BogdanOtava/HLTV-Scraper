from scraper.team_rankings_scraper import get_team_rankings
from scraper.news_scraper import get_news
from scraper.players_statistics_scraper import get_player_statistics

if __name__ == "__main__":
    get_team_rankings(2022, "november", 28)
    get_news(2022, "october")
    get_player_statistics()