import argparse
import json
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--sport", type=str, required=True)
parser.add_argument("--src", type=str, required=True)
parser.add_argument("--dwnld", action="store_true")
args = parser.parse_args()


def test(sport, src):
    from handlers.tables import MyTableMaker
    from handlers.visualizer import MyVisualizer
    from os.path import exists

    if not exists(f"data/{sport}.json"):
        raise Exception(
            f"data/{sport}.json does not exist, please download data first."
        )

    table_maker = MyTableMaker(sport, src)
    print(table_maker.get_sentiment_tbl())
    print(table_maker.get_rankings_tbl())
    print(table_maker.get_deviation_tbl())
    """visualizer = MyVisualizer(sport, src, static=True)
    visualizer.get_sentiment_bar()
    visualizer.get_sentiment_dist()
    visualizer.get_sentiment_box_and_whisker()
    visualizer.get_rankings_dist()
    visualizer.get_rankings_bar()
    visualizer.get_deviation_bar()"""


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
        if args.src == "twitter":
            data = asyncio.run(handler.get_full_data())
        elif args.src == "reddit":
            data = handler.get_full_data()
        json.dump(data, open(f"{args.src}_data/{sport}.json", "w"))

    # test(sport, args.src)
