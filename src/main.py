from Game import Game
import Mail
import Scraping


def notify():
    html = [Game.fromJson(html).asHtml() for html in Scraping.getFreeGames()]
    Mail.sendMails(html)


if __name__ == "__main__":
    notify()
