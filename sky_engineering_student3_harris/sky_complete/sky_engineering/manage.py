#!/usr/bin/env python

import os
import sys


def main():
    # Tell Django which settings module to load for this project.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sky_engineering.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # This error usually means Django is not installed or the virtual
        # environment has not been activated.
        raise ImportError(
            "Couldn't import Django. Make sure it is installed and available "
            "on your PYTHONPATH environment variable. Did you forget to activate "
            "a virtual environment?"
        ) from exc

    # Pass the terminal command through to Django.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
