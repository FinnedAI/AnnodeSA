import argparse
import json
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--sport", type=str, required=True)
parser.add_argument("--src", type=str, required=True)
parser.add_argument("--dwnld", action="store_true")
args = parser.parse_args()

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
