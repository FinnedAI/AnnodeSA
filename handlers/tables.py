import json
import pandas as pd


class MyTableMaker:
    def __init__(self, sport):
        self.sport = sport
        self.data = self.get_data()

    def get_data(self):
        data = json.load(open(f"data/{self.sport}.json", "r"))
        for team in data:
            data[team] = [x for x in data[team] if x["sentiment"] != 0]
        return data

    def get_sentiment_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["sentiment"] = [
            sum([x["sentiment"] for x in self.data[team]])
            / (len(self.data[team]) if len(self.data[team]) != 0 else 1)
            for team in self.data
        ]

        return df.sort_values(by="sentiment", ascending=False)

    def get_normed_sentiment_tbl(self):
        df = self.get_sentiment_tbl()
        new_df = pd.DataFrame()
        mu = df["sentiment"].mean()
        sigma = df["sentiment"].std()
        new_df["team"] = df["team"]
        new_df["sentiment"] = [(x - mu) / sigma for x in df["sentiment"]]
        return new_df.sort_values(by="sentiment", ascending=False)

    def get_rankings_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["ranking"] = [
            sum([x["ranking"] for x in self.data[team]])
            / (len(self.data[team]) if len(self.data[team]) != 0 else 1)
            for team in self.data
        ]

        return df.sort_values(by="ranking", ascending=False)

    def get_normed_rankings_tbl(self):
        df = self.get_rankings_tbl()
        new_df = pd.DataFrame()
        mu = df["ranking"].mean()
        sigma = df["ranking"].std()
        new_df["team"] = df["team"]
        new_df["ranking"] = [(x - mu) / sigma for x in df["ranking"]]
        return new_df.sort_values(by="ranking", ascending=False)

    def get_deviation_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        sentiment = self.get_normed_sentiment_tbl()
        rankings = self.get_normed_rankings_tbl()
        df["deviation"] = [
            abs(
                sentiment[sentiment["team"] == team]["sentiment"].values[0]
                - rankings[rankings["team"] == team]["ranking"].values[0]
            )
            for team in self.data
        ]

        return df.sort_values(by="deviation", ascending=False)
