"""
Crane Lifting Capacity Management Script

This is the main entrypoint for managing crane data in the
Crane Lifting Capacity application.
It provides a command-line interface for development purposes
for database operations and data management tasks.

Available Commands:
    populate-db: Import crane data from Excel files and attachments into the
                 database
    dump-cranes: Export crane data from database to JSON files
    show-cranes-summary: Display summary of all cranes in database

Usage Examples:
    # Populate database from default data directory
    python manage.py populate-db

    # Populate database from specific data directory
    python manage.py populate-db --data-dir /path/to/data/dir

    # Populate database with custom database URL
    python manage.py populate-db --database-url postgresql://user:pass@localhost/cranes

    # Display summary of cranes in database
    python manage.py show-cranes-summary

    # Display summary with custom database URL
    python manage.py show-cranes-summary --database-url postgresql://user:pass@localhost/cranes

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
    python manage.py show-cranes-summary --help

Environment Variables:
    The script uses the following environment variables
    (can be overridden with CLI args):
    - DATA_DIR: Default directory containing cranes data files for import
    - DATABASE_URL: Default database connection URL

Examples with Environment Variables:
    # Set environment variables in .env file
    DATA_DIR=/path/to/data/dir
    DATABASE_URL=postgresql://user:pass@localhost/cranes

    # Then use simple commands
    python manage.py populate-db  # Uses DATA_DIR and DATABASE_URL from .env
    python manage.py show-cranes-summary  # Uses DATABASE_URL from .env
    python manage.py dump-cranes  # Uses DATABASE_URL from .env

Data Format Requirements:
    Excel files must follow this structure:
    - A1: "Модель" (Model)             B1: model value
    - A2: "Производитель" (Manufacturer) B2: manufacturer value
    - A3: "Тип" (Type)                 B3: chassis_type value
    - A4: "Сборник" (Pricebook)        B4: pricebook value
    - A5: "Код ресурса" (Resource Code) B5: resource_code value
    - D1: "Сметная цена без учета оплаты труда" (Base Price)
    - D2: base_price value
    - D3: "Оплата труда машинистов" (Labor Cost)
    - D4: labor_cost value
    - D5: "Максимальная грузоподъемность" (Max Lifting Capacity)
         G5: max_lifting_capacity value
    - B8: Lifting capacity table starts here

    Attachments should be stored in data/attachments/{crane_type}/ directory
    with files named as {manufacturer}_{model}.{extension}

Error Handling:
- Unknown commands are reported with helpful error messages
- Missing required arguments show appropriate help text
- Database connection errors are handled gracefully
- Excel parsing errors are logged with file details
- Attachment processing errors are handled gracefully
"""

from dev_scripts.cli_parser import parse_and_execute


def main():
    parse_and_execute()


if __name__ == "__main__":
    main()
