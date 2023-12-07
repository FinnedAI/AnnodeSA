import plotly.express as px
from handlers.common import MyCommonOps
import numpy as np
import pandas as pd
import json
import scipy.stats as stats


# Visualizes and analyzes sports data with a focus on sentiment
class MyVisualizer:

    # Initializes class with sport type, data source, and common operations.
    def __init__(self, sport, src):
        self.sport = sport
        self.src = src
        self.common = MyCommonOps(sport, src)
        self.data = self.get_data()

    # loads and preprocess sports data from a JSON file
    def get_data(self):
        data = json.load(open(f"{self.src}_data/{self.sport}.json", "r"))
        for team in data:
            data[team] = [x for x in data[team] if x["sentiment"] != 0]
        return data

    # calculates and returns sentiment distribution
    # df stands for DataFrame, contains sentiment data
    def get_sentiment_dist(self, df):
        mu = df["sentiment"].mean()
        sigma = df["sentiment"].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)

        return pd.DataFrame(y, index=x)

    # generates a box and whisker plot for sentiment data
    def get_sentiment_box_and_whisker(self):
        data = [
            {"team": team, "sentiment": x["sentiment"]}
            for team in self.data
            for x in self.data[team]
        ]
        data = pd.DataFrame(data)
        data["team"] = data["team"].apply(self.common.get_screen_name)
        plt = px.box(data, x="team", y="sentiment")

        return plt

    # calculates and returns rankings distribution
    def get_rankings_dist(self, df):
        mu = df["ranking"].mean()
        sigma = df["ranking"].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)

        return pd.DataFrame(y, index=x)
