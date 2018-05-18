"""Resources for Version 3 of the Storage Service API.

Defines the following sub-classes of ``drl.Resources``:

- ``Packages``
- ``Locations``
- ``Pipelines``
- ``Spaces``
"""

import logging

from locations.api.v3.drl import utils, Resources
from locations.api.v3.schemata import (
    LocationSchema,
    PackageSchema,
    SpaceSchema,
    PipelineSchema,
)
from locations.models import (
    Location,
    Package,
    Space,
    Pipeline,
)

logger = logging.getLogger(__name__)


class SSResources(Resources):

    @property
    def resource_collections(self):
        return {
            'package_types': self.RsrcColl(
                model_cls='',
                getter=lambda: self.model_cls.PACKAGE_TYPE_CHOICES),
            'package_statuses': self.RsrcColl(
                model_cls='',
                getter=lambda: self.model_cls.STATUS_CHOICES),
            'space_access_protocols': self.RsrcColl(
                model_cls='',
                getter=lambda: self.model_cls.ACCESS_PROTOCOL_CHOICES),
            'location_purposes': self.RsrcColl(
                model_cls='',
                getter=lambda: self.model_cls.PURPOSE_CHOICES),
            'packages': self.RsrcColl(
                model_cls=Package,
                getter=self.get_mini_dicts_getter(Package)),
            'pipelines': self.RsrcColl(
                model_cls=Pipeline,
                getter=self.get_mini_dicts_getter(Pipeline)),
            'locations': self.RsrcColl(
                model_cls=Location,
                getter=self.get_mini_dicts_getter(Location)),
            'spaces': self.RsrcColl(
                model_cls=Space,
                getter=self.get_mini_dicts_getter(Space)),
        }


class Packages(SSResources):

    model_cls = Package
    schema_cls = PackageSchema

    def _get_user_data(self, data):
        return {
            'description': utils.normalize(data['description']),
        }

    def _get_create_data(self, data):
        return self._get_update_data(self._get_user_data(data))

    def _get_update_data(self, user_data):
        user_data.update({})
        return user_data

    def _get_new_edit_collections(self):
        """Returns the names of the collections that are required in order to
        create a new, or edit an existing, pipeline.
        """
        return (
            'package_types',
            'package_statuses',
            'locations',
            'packages',
            'pipelines',
        )


class Locations(SSResources):

    model_cls = Location
    schema_cls = LocationSchema

    def _get_user_data(self, data):
        return {
            'description': utils.normalize(data['description']),
        }

    def _get_create_data(self, data):
        return self._get_update_data(self._get_user_data(data))

    def _get_update_data(self, user_data):
        user_data.update({})
        return user_data


class Pipelines(SSResources):

    model_cls = Pipeline
    schema_cls = PipelineSchema

    def _get_user_data(self, data):
        return {
            'description': utils.normalize(data['description']),
        }

    def _get_create_data(self, data):
        return self._get_update_data(self._get_user_data(data))

    def _get_update_data(self, user_data):
        user_data.update({})
        return user_data


class Spaces(SSResources):

    model_cls = Space
    schema_cls = SpaceSchema

    def _get_user_data(self, data):
        return {
            'path': utils.normalize(data['path']),
        }

    def _get_create_data(self, data):
        return self._get_update_data(self._get_user_data(data))

    def _get_update_data(self, user_data):
        user_data.update({})
        return user_data
