import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
from os.path import exists
from handlers.tables import MyTableMaker

reqs = ["nfl.json", "nba.json", "mlb.json", "nhl.json"]
for req in reqs:
    if not exists(f"data/{req}"):
        raise FileNotFoundError(
            f"Required data/{req} file does not exist. Please run main.py --dwnld to download the data."
        )


class MyVisualizer:
    def __init__(self, sport, static=False):
        self.sport = sport
        self.data = self.get_data()
        self.static = static
        self.table_maker = MyTableMaker(self.sport)

    def get_data(self):
        return json.load(open(f"data/{self.sport}.json", "r"))

    def get_sentiment_bar(self):
        df = self.table_maker.get_sentiment_tbl()
        x = df.index
        y = df[0]
        plt.bar(x, y)
        plt.title(f"{self.sport} Sentiment")
        plt.xlabel("Teams")
        plt.ylabel("Sentiment")

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment.png")
        else:
            plt.show()

    def get_sentiment_dist(self):
        df = self.table_maker.get_sentiment_tbl()
        mu = df[0].mean()
        sigma = df[0].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, y)
        plt.title(f"{self.sport} Sentiment")
        plt.xlabel("Sentiment")
        plt.ylabel("Number of Teams")

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment.png")
        else:
            plt.show()

    def get_sentiment_box_and_whisker(self):
        df = self.table_maker.get_sentiment_tbl()
        plt.boxplot(df[0])
        plt.title(f"{self.sport} Sentiment")
        plt.ylabel("Sentiment")

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment.png")
        else:
            plt.show()

    def get_rankings_dist(self):
        df = self.table_maker.get_rankings_tbl()
        mu = df["ranking"].mean()
        sigma = df["ranking"].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, y)
        plt.title(f"{self.sport} Rankings")
        plt.xlabel("Rankings")
        plt.ylabel("Number of Teams")

        if self.static:
            plt.savefig(f"static/{self.sport}_rankings.png")
        else:
            plt.show()

    def get_deviation_bar(self):
        df = self.get_deviation_tbl()
        x = df.index
        y = df[0]
        plt.bar(x, y)
        plt.title(f"{self.sport} Deviation of Sentiment to Actual Ranking")
        plt.xlabel("Teams")
        plt.ylabel("Deviation")

        if self.static:
            plt.savefig(f"static/{self.sport}_deviation.png")
        else:
            plt.show()
