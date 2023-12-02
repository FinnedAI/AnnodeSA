import json
import pandas as pd
from os.path import exists

reqs = ["nfl.json", "nba.json", "mlb.json", "nhl.json"]
for req in reqs:
    if not exists(f"data/{req}"):
        raise FileNotFoundError(
            f"Required data/{req} file does not exist. Please run main.py --dwnld to download the data."
        )


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
            sum([x["sentiment"] for x in self.data[team]]) / len(self.data[team])
            for team in self.data
        ]

        return df.sort_values(by="sentiment", ascending=False)

    def get_rankings_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["ranking"] = [
            sum([x["ranking"] for x in self.data[team]]) / len(self.data[team])
            for team in self.data
        ]

        return df.sort_values(by="ranking", ascending=False)

    def get_deviation_tbl(self):
        df = pd.DataFrame()
        df["team"] = list(self.data.keys())
        df["deviation"] = [
            abs(
                sum([x["ranking"] for x in self.data[team]]) / len(self.data[team])
                - sum([x["sentiment"] for x in self.data[team]]) / len(self.data[team])
            )
            for team in self.data
        ]

        return df.sort_values(by="deviation", ascending=False)
