import argparse

from .dump_cranes_data import dump_cranes_summary, dump_cranes_to_json
from .populate_db_from_xlsx import populate_db_from_excel


def create_parser():
    """
    Create and configure the argument parser for crane management commands.

    Returns:
        argparse.ArgumentParser: Parser with populate-db and dump-cranes
        subcommands
    """
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
    populate_parser.add_argument(
        "--data-dir",
        help="Directory containing Excel files "
        "(if not provided, will use DATA_DIR from .env)",
    )
    populate_parser.add_argument(
        "--database-url",
        help="Database URL (if not provided, will use DATABASE_URL from .env)",
    )

    # Add dump-cranes command
    dump_cranes_parser = subparsers.add_parser(
        "dump-cranes",
        help="Dump existing cranes data from database to separate JSON files",
    )
    dump_cranes_parser.add_argument(
        "--output-dir",
        help="Output directory path (default: cranes_dump in script "
        "directory)",
    )
    dump_cranes_parser.add_argument(
        "--database-url",
        help="Database URL (if not provided, will use DATABASE_URL from .env)",
    )
    dump_cranes_parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Print summary only, don't create JSON files",
    )

    return parser


def handle_populate_db(args):
    """
    Handle the populate-db command.

    Args:
        args: Parsed arguments containing data_dir and database_url options
    """
    populate_db_from_excel(
        data_dir=args.data_dir, database_url=args.database_url
    )


def handle_dump_cranes(args):
    """
    Handle the dump-cranes command.

    Args:
        args: Parsed arguments containing output_dir, database_url, and
            summary_only options
    """
    if args.summary_only:
        dump_cranes_summary(database_url=args.database_url)
    else:
        dump_cranes_to_json(
            database_url=args.database_url,
            output_dir=args.output_dir,
        )


def parse_and_execute():
    """
    Parse command line arguments and execute the appropriate command.

    Routes to populate-db or dump-cranes handlers based on the command.
    Shows help if no command is provided or if an unknown command is used.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "populate-db":
        handle_populate_db(args)
    elif args.command == "dump-cranes":
        handle_dump_cranes(args)
    elif not args.command:
        parser.print_help()
    else:
        print(f"Unknown command: {args.command}")
