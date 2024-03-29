import json
import pandas as pd
from twscrape import API, gather
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging
import requests

hashtags = json.load(open("config/translated_twitter.json"))
credentials = json.load(open("config/credentials.json"))


# Handles login and scraping of tweets using provided APIs and credentials.
class MyAppLogic:
    async def login(self):
        self.api = API()
        for user in credentials["users"]:
            await self.api.pool.add_account(
                user["tw_user"], user["tw_pass"], user["mail_user"], user["mail_pass"]
            )
        await self.api.pool.login_all()

    def _get_comment_sentiment(self, comment):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(comment)["compound"]

    async def scrape_tweets(self, hashtag):
        out = pd.DataFrame()
        texts, dates = [], []
        tweets = await gather(
            self.api.search(
                f"#{hashtag} -filter:media filter:replies within_time:7d", limit=100
            )
        )
        for tweet in tweets:
            texts.append(tweet.rawContent)
            date = tweet.date
            dates.append(f"{date.year}{date.month}{date.day}")

        out["text"] = texts
        out["date"] = dates

        return out


# Manages sports data handling including login, fetching rankings, comments, and sentiments.
class MyDataHandler:
    def __init__(self, sport):
        self.sport = sport
        self.backend = MyAppLogic()
        self.hashes = hashtags[sport]
        self.data = {}

    async def login(self):
        await self.backend.login()

    def _get_finned_rankings(self):
        url = "https://fpd.finned.tech/rankings.json"
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"Could not get rankings, got {r.status_code}")

        rankings = r.json()[self.sport]
        for team, hashtag in self.hashes.items():
            if team not in rankings:
                logging.warning(f"Could not find {team} in rankings")
                rankings[team] = 0.5

            if hashtag not in self.data:
                self.data[hashtag] = pd.DataFrame()
            rank = [rankings[team]] * 100
            self.data[hashtag]["ranking"] = rank

    async def _get_all_comments(self):
        for hashtag in self.hashes.values():
            if hashtag not in self.data:
                self.data[hashtag] = pd.DataFrame()

            posts = await self.backend.scrape_tweets(hashtag)
            if posts is None:
                continue

            self.data[hashtag]["comments"] = posts["text"]
            self.data[hashtag]["date"] = posts["date"]

    def _get_all_sentiments(self):
        for hashtag in self.data:
            self.data[hashtag] = self.data[hashtag].dropna()
            self.data[hashtag]["sentiment"] = [
                self.backend._get_comment_sentiment(comment)
                for comment in self.data[hashtag]["comments"]
            ]

    async def get_full_data(self):
        await self.login()

        self._get_finned_rankings()
        await self._get_all_comments()
        self._get_all_sentiments()
        for hashtag in self.data:
            self.data[hashtag] = self.data[hashtag].to_dict(orient="records")
        return self.data
