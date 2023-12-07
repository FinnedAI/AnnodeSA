import json
import pandas as pd


# Handles operations related to sports data, such as translation and data retrieval
class MyTableMaker:
    def __init__(self, sport, src):
        self.translator = json.load(open(f"config/translated_{src}.json", "r"))
        self.sport = sport
        self.src = src
        self.data = self.get_data()

    def get_screen_name(self, team):
        for k, v in self.translator[self.sport].items():
            if team == v:
                return k

    def get_data(self):
        data = json.load(open(f"{self.src}_data/{self.sport}.json", "r"))
        for team in data:
            data[team] = [x for x in data[team] if x["sentiment"] != 0]
        return data

    def get_sentiment_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["team"] = df["team"].apply(lambda x: self.get_screen_name(x))
        df["sentiment"] = [
            sum([x["sentiment"] for x in self.data[team]])
            / (len(self.data[team]) if len(self.data[team]) != 0 else 1)
            for team in self.data
        ]

        df = df[df["team"].notna()].set_index("team")
        return df.sort_values(by="sentiment", ascending=False)

    def get_normed_sentiment_tbl(self):
        df = self.get_sentiment_tbl()
        new_df = pd.DataFrame()
        mu = df["sentiment"].mean()
        sigma = df["sentiment"].std()
        new_df["team"] = df.index
        new_df["sentiment"] = [(x - mu) / sigma for x in df["sentiment"]]
        new_df = new_df[new_df["team"].notna()].set_index("team")
        return new_df.sort_values(by="sentiment", ascending=False)
    # Gets normalized sentiment

    def get_rankings_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["team"] = df["team"].apply(lambda x: self.get_screen_name(x))
        df["ranking"] = [
            sum([x["ranking"] for x in self.data[team]])
            / (len(self.data[team]) if len(self.data[team]) != 0 else 1)
            for team in self.data
        ]
        # Gets Rankings

        df = df[df["team"].notna()].set_index("team")
        return df.sort_values(by="ranking", ascending=False)

    def get_normed_rankings_tbl(self):
        df = self.get_rankings_tbl()
        new_df = pd.DataFrame()
        mu = df["ranking"].mean()
        sigma = df["ranking"].std()
        new_df["team"] = df.index
        new_df["ranking"] = [(x - mu) / sigma for x in df["ranking"]]
        new_df = new_df[new_df["team"].notna()].set_index("team")
        return new_df.sort_values(by="ranking", ascending=False)

    def get_deviation_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["team"] = df["team"].apply(lambda x: self.get_screen_name(x))
        sentiment = self.get_normed_sentiment_tbl()
        rankings = self.get_normed_rankings_tbl()

        deviation = []
        for team in df["team"]:
            s = sentiment[sentiment.index == team]["sentiment"].values
            r = rankings[rankings.index == team]["ranking"].values
            s = s[0] if len(s) > 0 else 0
            r = r[0] if len(r) > 0 else 0

            deviation.append(abs(r - s))

        df["deviation"] = deviation
        df = df[df["team"].notna()].set_index("team")
        return df.sort_values(by="deviation", ascending=False)
