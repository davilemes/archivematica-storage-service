# -*- coding: utf-8 -*-

"""Management command that creates an OpenAPI YAML file describing the V3
API.

To run from a Docker Compose deploy::

    $ docker-compose exec archivematica-storage-service /src/storage_service/manage.py apiv3openapi

"""

import django
from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from locations.api.v3 import drl

def main():
    drl.generate_open_api_yaml()
    return 0


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
