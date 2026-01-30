"""
Command Line Interface Parser for Crane Management Scripts

This module provides the command-line interface for the crane management
system. It handles argument parsing and routing to appropriate handlers for
different operations like populating the database, dumping crane data, and
showing summaries.

Available Commands:
    populate-db: Import crane data from Excel files and attachments
    dump-cranes: Export crane data to JSON files
    show-cranes-summary: Display summary of all cranes in database

Command Structure:
    python manage.py <command> [options]

Examples:
    python manage.py populate-db --data-dir /path/to/data
    python manage.py dump-cranes --output-dir /path/to/output
    python manage.py show-cranes-summary

Arguments:
    populate-db:
        --data-dir: Directory containing Excel files and attachments
        --database-url: Database connection URL

    dump-cranes:
        --output-dir: Directory for JSON output files
        --database-url: Database connection URL

    show-cranes-summary:
        --database-url: Database connection URL

Environment Variables:
    - ATTACHMENTS_DIR: Default data directory for populate-db
    - DATABASE_URL: Default database URL for all commands

Error Handling:
    - Validates required arguments and environment variables
    - Provides helpful error messages for missing parameters
    - Routes unknown commands to help display
"""

import argparse

from .dump_cranes_data import dump_cranes_to_json
from .populate_db_with_cranes.main import populate_db
from .show_cranes_summary import show_cranes_summary


def create_parser():
    """
    Create and configure the argument parser for crane management commands.

    Returns:
        argparse.ArgumentParser: Parser with populate-db, dump-cranes, and
        show-cranes-summary subcommands
    """
    parser = argparse.ArgumentParser(
        description="Crane Lifting Capacity management commands"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Add populate-db command
    populate_parser = subparsers.add_parser(
        "populate-db", help="Populate database with cranes data"
    )
    populate_parser.add_argument(
        "--cranes-dir",
        help="Directory containing cranes data files "
        "(if not provided, will use CRANES_DIR from settings)",
    )
    populate_parser.add_argument(
        "--database-url",
        help="Database URL (if not provided, will use DATABASE_URL from "
        "settings)",
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
        help="Database URL (if not provided, will use DATABASE_URL from "
        "settings)",
    )

    # Add show-cranes-summary command
    show_summary_parser = subparsers.add_parser(
        "show-cranes-summary",
        help="Display summary of all cranes in database",
    )
    show_summary_parser.add_argument(
        "--database-url",
        help="Database URL (if not provided, will use DATABASE_URL from "
        "settings)",
    )

    return parser


def handle_populate_db(args):
    """
    Handle the populate-db command.

    Args:
        args: Parsed arguments containing cranes_dir and database_url options
    """
    populate_db(cranes_dir=args.cranes_dir, database_url=args.database_url)


def handle_dump_cranes(args):
    """
    Handle the dump-cranes command.

    Args:
        args: Parsed arguments containing output_dir and database_url options
    """
    dump_cranes_to_json(
        database_url=args.database_url,
        output_dir=args.output_dir,
    )


def handle_show_cranes_summary(args):
    """
    Handle the show-cranes-summary command.

    Args:
        args: Parsed arguments containing database_url option
    """
    show_cranes_summary(database_url=args.database_url)


def parse_and_execute():
    """
    Parse command line arguments and execute the appropriate command.

    Routes to populate-db, dump-cranes, or show-cranes-summary handlers
    based on the command. Shows help if no command is provided or if an
    unknown command is used.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "populate-db":
        handle_populate_db(args)
    elif args.command == "dump-cranes":
        handle_dump_cranes(args)
    elif args.command == "show-cranes-summary":
        handle_show_cranes_summary(args)
    elif not args.command:
        parser.print_help()
    else:
        print(f"Unknown command: {args.command}")
