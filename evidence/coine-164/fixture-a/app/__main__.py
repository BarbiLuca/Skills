import argparse

from app.db import Database


def main() -> None:
    parser = argparse.ArgumentParser(prog="rates")
    subcommands = parser.add_subparsers(dest="command", required=True)
    list_parser = subcommands.add_parser("list", help="List stored rates for a base currency")
    list_parser.add_argument("base")
    args = parser.parse_args()

    database = Database()
    database.init_schema()
    if args.command == "list":
        for row in database.list_rates(args.base):
            print(f"{row['base']}/{row['quote']} {row['rate']} ({row['fetched_at']})")


if __name__ == "__main__":
    main()
