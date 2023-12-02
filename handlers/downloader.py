import json
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging
import requests
import time

subreddits = json.load(open("config/translated_names.json"))


class MyAppLogic:
    def _get_comment_sentiment(self, comment):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(comment)["compound"]

    def scrape_subreddit(self, subreddit):
        out = pd.DataFrame()
        titles, texts, dates = [], [], []
        r = requests.get(
            f"https://www.reddit.com/r/{subreddit}.json?limit=100",
            headers={"User-agent": "Mozilla/5.0", "Content-Type": "application/json"},
        )
        if r.status_code == 429:
            logging.warning("Too many requests, sleeping for 3 minutes.")
            time.sleep(180)
            return self.scrape_subreddit(subreddit)

        if r.status_code != 200:
            logging.warning(f"Could not scrape {subreddit}, got {r.status_code}")
            return None

        for post in r.json()["data"]["children"]:
            if "title" not in post["data"]:
                logging.warning(f"Empty post in {subreddit}")
                continue

            if "selftext" not in post["data"]:
                logging.warning(f"Empty post in {subreddit}")
                continue

            titles.append(post["data"]["title"])
            texts.append(" " + post["data"]["selftext"])
            created = post["data"]["created_utc"]
            dates.append(time.strftime("%Y%m%d", time.gmtime(created)))

        if len(texts) < 100:
            logging.warning(f"Only {len(texts)} posts in {subreddit}")
            return None

        out["title"] = titles[:100]
        out["text"] = texts[:100]
        out["date"] = dates[:100]

        time.sleep(5)
        return out


class MyDataHandler:
    def __init__(self, sport):
        self.sport = sport
        self.backend = MyAppLogic()
        self.subreddits = subreddits[sport]
        self.data = {}

    def _get_finned_rankings(self):
        url = "https://fpd.finned.tech/rankings.json"
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"Could not get rankings, got {r.status_code}")

        rankings = r.json()[self.sport]
        for team, subreddit in self.subreddits.items():
            if team not in rankings:
                logging.warning(f"Could not find {team} in rankings")
                rank = [0.66] * 100
                continue

            if subreddit not in self.data:
                self.data[subreddit] = pd.DataFrame()
            rank = [rankings[team]] * 100
            self.data[subreddit]["ranking"] = rank

    def _get_all_comments(self):
        for subreddit in self.subreddits.values():
            if subreddit not in self.data:
                self.data[subreddit] = pd.DataFrame()

            posts = self.backend.scrape_subreddit(subreddit)
            if posts is None:
                continue

            # comments is a combination of title and text
            comments = posts["title"] + posts["text"]
            self.data[subreddit]["comments"] = comments
            self.data[subreddit]["date"] = posts["date"]

    def _get_all_sentiments(self):
        for subreddit in self.data:
            self.data[subreddit]["sentiment"] = [
                self.backend._get_comment_sentiment(comment)
                for comment in self.data[subreddit]["comments"]
            ]

    def get_full_data(self):
        self._get_finned_rankings()
        self._get_all_comments()
        self._get_all_sentiments()
        for subreddit in self.data:
            self.data[subreddit] = self.data[subreddit].to_dict(orient="records")
        return self.data
