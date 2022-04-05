from datetime import datetime
import yagmail
import json
import os.path

sender: str
receivers: list
yag: yagmail.SMTP
SUBJECT = "Epic Free Games for " + datetime.date(datetime.now())


def send(receiver: str, body) -> None:
    yag.send(to=receiver, subject=SUBJECT, contents=body)


def sendMails(body) -> None:
    for receiver in receivers:
        yag.send(to=receiver, subject=SUBJECT, contents=body)


def getConfig() -> None:
    global sender, receivers
    with open(os.path.dirname(__file__) + "/../config.json", "r") as file:
        config = json.loads(file.read())
    sender = config["sender"]
    receivers = config["receivers"]


def setup() -> None:
    global yag
    getConfig()
    yag = yagmail.SMTP(sender)


setup()
