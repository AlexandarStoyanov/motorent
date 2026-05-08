import os
import sys
from pathlib import Path
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        natural_foreign=True,
        natural_primary=True,
        exclude=["contenttypes", "auth.permission"],
        indent=2,
        stdout=f,
    )