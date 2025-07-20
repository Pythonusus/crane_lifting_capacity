"""
Crane Lifting Capacity Management Script

This is the main entrypoint for managing crane data in the
Crane Lifting Capacity application.
It provides a command-line interface for development purposes
for database operations and data management tasks.

Available Commands:
    populate-db: Import crane data from Excel files into the database
    dump-cranes: Export crane data from db to JSON files or display summary

Usage Examples:
    # Populate database from Excel files in default data directory
    python manage.py populate-db

    # Populate database from specific directory
    python manage.py populate-db --data-dir /path/to/excel/files

    # Populate database with custom database URL
    python manage.py populate-db --database-url postgresql://user:pass@localhost/cranes

    # Display summary of cranes in database
    python manage.py dump-cranes --summary-only

    # Export all cranes to JSON files in default directory
    python manage.py dump-cranes

    # Export cranes to specific output directory
    python manage.py dump-cranes --output-dir /path/to/output

    # Export with custom database URL
    python manage.py dump-cranes --database-url postgresql://user:pass@localhost/cranes

    # Show help for all commands
    python manage.py

    # Show help for specific command
    python manage.py populate-db --help
    python manage.py dump-cranes --help

Environment Variables:
    The script uses the following environment variables
    (can be overridden with CLI args):
    - DATA_DIR: Default directory containing Excel files for import
    - DATABASE_URL: Default database connection URL

Examples with Environment Variables:
    # Set environment variables in .env file
    DATA_DIR=/path/to/excel/files
    DATABASE_URL=postgresql://user:pass@localhost/cranes

    # Then use simple commands
    python manage.py populate-db  # Uses DATA_DIR and DATABASE_URL from .env
    python manage.py dump-cranes --summary-only  # Uses DATABASE_URL from .env

Error Handling:
- Unknown commands are reported with helpful error messages
- Missing required arguments show appropriate help text
- Database connection errors are handled gracefully
"""

from dev_scripts.cli_parser import parse_and_execute


def main():
    parse_and_execute()


if __name__ == "__main__":
    main()
