from datetime import datetime
from collections import defaultdict
from os.path import dirname
import Scraping


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
    timestamp: str

    def __init__(self, originalPrice, discountPrice, name, description, freeUntil, imgUrl, storeUrl) -> None:
        self.originalPrice = originalPrice
        self.discountPrice = discountPrice
        self.name = name
        self.description = description
        self.freeUntil = self.format_time(freeUntil)
        self.imgUrl = imgUrl
        self.storeUrl = storeUrl
        self.genresFeaturesHtml = Game.__genresFeaturesAsHtml(
            Scraping.getGenresFeatures(storeUrl))
        self.htmlTemplate = Game.__readHtmlTemplate()
        self.timestamp = datetime.now()

    def asHtml(self) -> str:
        LF = "\n"
        html = self.htmlTemplate.replace(LF, '')
        html = f"{self.htmlTemplate.replace(LF, '')}".format(**self.__dict__)
        return html

    def format_time(self, time):
        def ordinal(num):
            ordinal_dict = defaultdict(lambda: "th")
            ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
            q, mod = divmod(num, 10)
            suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
            return f"{num}{suffix}"

        def weekday(num):
            weekdays = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
            return weekdays[num]

        time = datetime.strptime(
            time, "%Y-%m-%dT%H:%M:%S.%fZ")
        return f"{weekday(time.weekday())} the {ordinal(time.day)}"

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
    def __findStoreUrl(json: dict) -> str:
        BASE_URL = "https://store.epicgames.com/en-US/p/"
        try:
            if json["productSlug"].endswith("/home"):
                productSlug = productSlug.replace("/home", "")
                return BASE_URL + productSlug
        except:
            pass

        if json["catalogNs"]["mappings"][0]["pageType"] == "productHome":
            return BASE_URL + json["catalogNs"]["mappings"][0]["pageSlug"]

        if json["offerMappings"]["mappings"][0]["pageType"] == "productHome":
            return BASE_URL + json["offerMappings"]["mappings"][0]["pageSlug"]

    @staticmethod
    def fromJson(json: dict):
        originalPrice = json["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
        discountPrice = json["price"]["totalPrice"]["fmtPrice"]["discountPrice"]
        freeUntil = json["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
        imgUrl = Game.__findThumbnailUrl(json["keyImages"])

        urlJsonLocations = ["productSlug", "catalogNs", "offerMappings"]
        possibleUrlLocations = {key: json[key] for key in urlJsonLocations}
        storeUrl = Game.__findStoreUrl(possibleUrlLocations)

        return Game(originalPrice, discountPrice, json["title"], json["description"], freeUntil, imgUrl, storeUrl)
