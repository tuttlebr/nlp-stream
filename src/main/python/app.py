from TwitterAPI import TwitterAPI
from os import getenv
from logging import info, basicConfig
from datetime import datetime
from inference_management import *
import numpy as np
import re


CONSUMER_KEY = getenv("CONSUMER_KEY")
CONSUMER_SECRET = getenv("CONSUMER_SECRET")
ACCESS_TOKEN_KEY = getenv("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = getenv("ACCESS_TOKEN_SECRET")
TRACK_TERM = getenv("TRACK_TERM")
TIMESTAMP = datetime.now()
LOG_ID = TIMESTAMP.strftime("%Y%m%d_%H%M%S")
COMPREHENSION_ENGINE = ZeroComprehensionEngine()
TRACK_ENTAILMENTS = getenv("TRACK_ENTAILMENTS")

basicConfig(
    filename="/logs/{}.log".format(LOG_ID),
    level="INFO",
    format="%(asctime)s, %(message)s",
    datefmt="%H:%M:%S",
)


def clean_tweet(tweet):
    if type(tweet) == np.float:
        return ""
    temp = tweet.lower()
    temp = re.sub("'", "", temp)
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
    temp = temp.split()
    temp = " ".join(word for word in temp)
    return temp.replace("\n", "")

api = TwitterAPI(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
)

r = api.request("statuses/filter", {"track": TRACK_TERM})
info("comment,{},sentiment".format(TRACK_ENTAILMENTS))
for item in r:
    message = item["text"] if "text" in item else item
    message = clean_tweet(message)
    message = COMPREHENSION_ENGINE.free_comprehend(
        message, TRACK_ENTAILMENTS.split(",")
    )

    info(message)
