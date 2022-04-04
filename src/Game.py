from posixpath import dirname
import Scraping
from os.path import dirname


class Game:
    originalPrice: str
    discountPrice: str
    name: str
    description: str
    freeUntil: str
    imgUrl: str
    storeUrl: str
    htmlTemplate: str
    genresFeaturesHtml: str

    def __init__(self, originalPrice, discountPrice, name, description, freeUntil, imgUrl, storeUrl) -> None:
        self.originalPrice = originalPrice
        self.discountPrice = discountPrice
        self.name = name
        self.description = description
        self.freeUntil = freeUntil
        self.imgUrl = imgUrl
        self.storeUrl = storeUrl
        self.genresFeaturesHtml = Game.__genresFeaturesAsHtml(
            Scraping.getGenresFeatures(storeUrl))
        self.htmlTemplate = Game.__readHtmlTemplate()

    def asHtml(self) -> str:
        LF = "\n"
        html = self.htmlTemplate.replace(LF, '')
        html = f"{self.htmlTemplate.replace(LF, '')}".format(**self.__dict__)
        return html

    @staticmethod
    def __readHtmlTemplate() -> str:
        with open(dirname(__file__) + "/template.html", "r") as file:
            htmlTemplate = file.read()
        return htmlTemplate

    @staticmethod
    def __genresFeaturesAsHtml(genresFeatures: list) -> str:
        html = ""
        for item in genresFeatures:
            html += "<li>" + item + "</li>"
        return html

    @staticmethod
    def __findThumbnailUrl(imagesJson: list) -> str:
        for image in imagesJson:
            if image["type"] == "Thumbnail":
                return image["url"]
        return ""

    @staticmethod
    def __findStoreUrl(productSlug: str) -> str:
        if productSlug.endswith("/home"):
            productSlug = productSlug.replace("/home", "")
        return "https://store.epicgames.com/en-US/p/" + productSlug

    @staticmethod
    def fromJson(json: dict):
        originalPrice = json["price"]["totalPrice"]["originalPrice"]
        discountPrice = json["price"]["totalPrice"]["discountPrice"]
        freeUntil = json["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
        imgUrl = Game.__findThumbnailUrl(json["keyImages"])
        storeUrl = Game.__findStoreUrl(json["productSlug"])
        return Game(originalPrice, discountPrice, json["title"], json["description"], freeUntil, imgUrl, storeUrl)
