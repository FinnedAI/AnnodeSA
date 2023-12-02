import argparse
import json
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--sport", type=str, required=True)
parser.add_argument("--src", type=str, required=True)
parser.add_argument("--dwnld", action="store_true")
args = parser.parse_args()


def test():
    from handlers.tables import MyTableMaker
    from handlers.visualizer import MyVisualizer

    sport = args.sport
    # table_maker = MyTableMaker(sport)
    visualizer = MyVisualizer(sport, static=True)
    visualizer.get_sentiment_bar()
    visualizer.get_sentiment_dist()
    visualizer.get_sentiment_box_and_whisker()
    visualizer.get_rankings_dist()
    visualizer.get_deviation_bar()


if __name__ == "__main__":
    if args.src not in ["twitter", "reddit"]:
        raise Exception("src must be 'twitter' or 'reddit'")

    if args.src == "twitter":
        from handlers.twitter_downloader import MyDataHandler
    elif args.src == "reddit":
        from handlers.reddit_downloader import MyDataHandler

    sport = args.sport
    dwnld = args.dwnld

    if dwnld:
        handler = MyDataHandler(sport)
        data = asyncio.run(handler.get_full_data())
        json.dump(data, open(f"data/{sport}.json", "w"))

    test()
