import matplotlib.pyplot as plt
import json
import numpy as np
import scipy.stats as stats
from handlers.tables import MyTableMaker


class MyVisualizer:
    def __init__(self, sport, src, static=False):
        plt.style.use("ggplot")
        plt.rcParams["figure.figsize"] = [15, 15]

        self.sport = sport
        self.data = self.get_data()
        self.static = static
        self.table_maker = MyTableMaker(self.sport, src)

    def get_data(self):
        data = json.load(open(f"data/{self.sport}.json", "r"))
        for team in data:
            data[team] = [x for x in data[team] if x["sentiment"] != 0]
        return data

    def get_sentiment_bar(self):
        plt.close()
        df = self.table_maker.get_normed_sentiment_tbl()
        df = df[df["team"].notna()]
        plt.bar(df["team"], df["sentiment"])
        plt.title(f"{self.sport} Sentiment")
        plt.xticks(rotation=90)
        plt.xlabel("Teams")
        plt.ylabel("Sentiment")

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment_bar.png")

        return plt

    def get_sentiment_dist(self):
        plt.close()
        df = self.table_maker.get_sentiment_tbl()
        mu = df["sentiment"].mean()
        sigma = df["sentiment"].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, y)
        plt.title(f"{self.sport} Sentiment")
        plt.xticks(rotation=90)
        plt.xlabel("Sentiment")
        plt.ylabel("Number of Teams")

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment_dist.png")

        return plt

    def get_sentiment_box_and_whisker(self):
        plt.close()
        data = [[x["sentiment"] for x in self.data[team]] for team in self.data]
        fig, ax = plt.subplots()
        ax.boxplot(data)

        plt.title(f"{self.sport} Sentiment")
        plt.ylabel("Sentiment")
        plt.xlabel("Teams")

        labels = list(self.data.keys())
        plt.xticks(np.arange(1, len(labels) + 1), labels, rotation=90)

        if self.static:
            plt.savefig(f"static/{self.sport}_sentiment_baw.png")

        return plt

    def get_rankings_bar(self):
        plt.close()
        df = self.table_maker.get_normed_rankings_tbl()
        df = df[df["team"].notna()]
        plt.bar(df["team"], df["ranking"])
        plt.title(f"{self.sport} Rankings")
        plt.xticks(rotation=90)
        plt.xlabel("Teams")
        plt.ylabel("Rankings")

        if self.static:
            plt.savefig(f"static/{self.sport}_rankings_bar.png")

        return plt

    def get_rankings_dist(self):
        plt.close()
        df = self.table_maker.get_rankings_tbl()
        mu = df["ranking"].mean()
        sigma = df["ranking"].std()
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, y)
        plt.title(f"{self.sport} Rankings")
        plt.xticks(rotation=90)
        plt.xlabel("Rankings")
        plt.ylabel("Number of Teams")

        if self.static:
            plt.savefig(f"static/{self.sport}_rankings_dist.png")

        return plt

    def get_deviation_bar(self):
        plt.close()
        df = self.table_maker.get_deviation_tbl()
        df = df[df["team"].notna()]
        plt.bar(df["team"], df["deviation"])
        plt.title(f"{self.sport} Deviation of Sentiment to Actual Ranking")
        plt.xticks(rotation=90)
        plt.xlabel("Teams")
        plt.ylabel("Deviation")

        if self.static:
            plt.savefig(f"static/{self.sport}_deviation_bar.png")

        return plt
