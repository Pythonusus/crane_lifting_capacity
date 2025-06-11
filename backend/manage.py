import argparse

from dev_scripts.populate_db_from_xlsx import populate_db_from_excel


def main():
    parser = argparse.ArgumentParser(
        description="Crane Lifting Capacity management commands"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Add populate-db command
    populate_parser = subparsers.add_parser(
        "populate-db", help="Populate database from Excel files"
    )
    # Add arguments specific to populate-db command
    populate_parser.add_argument(
        "--data-dir",
        help="Directory containing Excel files \
        (if not provided, will use DATA_DIR from .env)",
    )
    populate_parser.add_argument(
        "--database-url",
        help="Database URL (if not provided, will use DATABASE_URL from .env)",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.command == "populate-db":
        populate_db_from_excel(
            data_dir=args.data_dir, database_url=args.database_url
        )
    elif not args.command:
        parser.print_help()
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
