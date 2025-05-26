#!/usr/bin/env python 
# # tells the system to use Python to run this file.
"""Django's command-line utility for administrative tasks."""
import os # is used to set environment variables.
import sys # is used to handle command-line arguments.

# function that runs admin tasks like server start, migrations, etc.
def main():
    """Run administrative tasks."""
    # This sets the default Django settings module (usually <project_name>.settings).Django needs to know where your settings are to run properly.

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FindJob.settings')
    try:
    # This imports the main Django function that reads commands (like runserver) and runs them.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) # This tells Django to execute the command you typed in the terminal, like:


if __name__ == '__main__':
    main()
