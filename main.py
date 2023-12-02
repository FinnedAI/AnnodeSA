import argparse
import json
from handlers.downloader import MyDataHandler
from handlers.tables import MyTableMaker
from handlers.visualizer import MyVisualizer

parser = argparse.ArgumentParser()
parser.add_argument("--sport", type=str, required=True)
parser.add_argument("--dwnld", action="store_true")
args = parser.parse_args()


def test():
    sport = args.sport
    table_maker = MyTableMaker(sport)
    visualizer = MyVisualizer(sport, static=True)
    print(table_maker.get_sentiment_tbl())
    print(table_maker.get_rankings_tbl())
    print(table_maker.get_deviation_tbl())
    visualizer.get_sentiment_bar()
    visualizer.get_sentiment_dist()
    visualizer.get_sentiment_box_and_whisker()
    visualizer.get_rankings_dist()
    visualizer.get_deviation_bar()


if __name__ == "__main__":
    sport = args.sport
    dwnld = args.dwnld

    if dwnld:
        data = MyDataHandler(sport).get_full_data()
        json.dump(data, open(f"data/{sport}.json", "w"))

    test()
