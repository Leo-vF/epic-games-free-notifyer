from requests import get
from bs4 import BeautifulSoup as bs
import json


def getFreeGames() -> list:
    url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=DE&allowCountries=DE"
    data = json.loads(get(url).text)
    games = data["data"]["Catalog"]["searchStore"]["elements"]

    for game in games[:]:
        if game["promotions"] == None:
            games.remove(game)
            continue
        promotion = game["promotions"]["promotionalOffers"]
        if len(promotion) == 0:
            games.remove(game)
        elif promotion[0]["promotionalOffers"][0]["discountSetting"]["discountPercentage"] != 0:
            games.remove(game)
    return games


def getGenresFeatures(url: str) -> list:
    rawHtml = get(url).text
    html = bs(rawHtml, "html.parser")
    genresFeaturesHtml: list[bs] = html.find_all(class_="css-t8k7")
    genresFeatures = []
    for item in genresFeaturesHtml:
        genresFeatures.append(
            item.find(attrs={"data-component": "Message"}).contents[0])
    return genresFeatures


if __name__ == "__main__":
    print(getGenresFeatures("https://store.epicgames.com/en-US/p/total-war-warhammer"))
