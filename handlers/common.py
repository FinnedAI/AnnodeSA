import numpy as np
import pandas as pd
import json


# Performs common operations on sports data, such as data retrieval and translation.
class MyCommonOps:
    def __init__(self, sport, src):
        self.sport = sport
        self.src = src
        self.data = self.get_data()
        self.translator = json.load(open(f"config/translated_{src}.json", "r"))

    def get_screen_name(self, team):
        for k, v in self.translator[self.sport].items():
            if team == v:
                return k

    def get_data(self):
        data = json.load(open(f"{self.src}_data/{self.sport}.json", "r"))
        for team in data:
            data[team] = [x for x in data[team] if x["sentiment"] != 0]
        return data

    def teams(self):
        return list(team for team in self.data.keys())

    def inverse_teams(self, inp, type="df"):
        if type == "df":
            return inp["team"].apply(lambda x: self.get_screen_name(x))
        elif type == "list":
            return [self.get_screen_name(x) for x in inp if x is not None]

    def avg(self, df, col):
        return df[col].mean()

    def std(self, df, col):
        return df[col].std()
