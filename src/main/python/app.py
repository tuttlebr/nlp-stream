import re
from datetime import datetime
from logging import basicConfig, info
from os import getenv

from inference_management import *
from searchtweets import (collect_results, gen_request_parameters,
                          load_credentials)

TRACK_TERM = getenv("TRACK_TERM")
TIMESTAMP = datetime.now()
LOG_ID = TIMESTAMP.strftime("%Y%m%d_%H%M%S")
COMPREHENSION_ENGINE = ZeroComprehensionEngine()
TRACK_ENTAILMENTS = getenv("TRACK_ENTAILMENTS")


def clean_tweet(tweet):
    temp = tweet.lower()
    temp = re.sub("'", "", temp)
    temp = re.sub("@[A-Za-z0-9_]+", "", temp)
    temp = re.sub("#[A-Za-z0-9_]+", "", temp)
    temp = re.sub(r"http\S+", "", temp)
    temp = re.sub("[()!?]", " ", temp)
    temp = re.sub("\[.*?\]", " ", temp)
    temp = re.sub("[^a-z0-9]", " ", temp)
    temp = temp.split()
    temp = " ".join(word for word in temp)
    return temp.replace("\n", "")


search_args = load_credentials(
    filename="/app/.twitter_keys.yaml",
    yaml_key="search_tweets_v2",
    env_overwrite=False,
)

query = gen_request_parameters(TRACK_TERM, results_per_call=100, granularity=None)
tweets = collect_results(query, max_tweets=5000, result_stream_args=search_args)

basicConfig(
    filename="/logs/{}.log".format(LOG_ID),
    level="INFO",
    format="%(asctime)s, %(message)s",
    datefmt="%H:%M:%S",
)
info("comment,{},sentiment".format(TRACK_ENTAILMENTS))


for tweet in tweets:
    for item in tweet["data"]:
        message = item["text"] if "text" in item else item
        message = clean_tweet(message)
        if len(message) > 10:
            message = COMPREHENSION_ENGINE.free_comprehend(
                message, TRACK_ENTAILMENTS.split(",")
            )

            info(message)
