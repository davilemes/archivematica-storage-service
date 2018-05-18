from collections import OrderedDict
import json
import pprint


from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyRel,
    ManyToManyField,
    ManyToOneRel,
    ManyToOneRel,
)
from django.db.models.fields import (
    AutoField,
    BigIntegerField,
    BooleanField,
    CharField,
    TextField,
)
from django_extensions.db.fields import UUIDField

django_field_class2openapi_type = {
    'AutoField': 'integer',
    'BigIntegerField': 'integer',
    'BooleanField': 'boolean',
    'CharField': 'string',
    'TextField': 'string',
    'UUIDField': 'string',
}
django_field_class2openapi_format = {
    'UUIDField': 'uuid',
}

"""
LocationView
- masters
  - <class 'django.db.models.fields.related.ManyToManyRel'>
- locationpipeline
  - <class 'django.db.models.fields.related.ManyToOneRel'>
- package
  - <class 'django.db.models.fields.related.ManyToOneRel'>
- id
  - <class 'django.db.models.fields.AutoField'>
- uuid
  - <class 'django_extensions.db.fields.UUIDField'>
- space
  - <class 'django.db.models.fields.related.ForeignKey'>
- purpose
  - <class 'django.db.models.fields.CharField'>
- relative_path
  - <class 'django.db.models.fields.TextField'>
- description
  - <class 'django.db.models.fields.CharField'>
- quota
  - <class 'django.db.models.fields.BigIntegerField'>
- used
  - <class 'django.db.models.fields.BigIntegerField'>
- enabled
  - <class 'django.db.models.fields.BooleanField'>
- pipeline
  - <class 'django.db.models.fields.related.ManyToManyField'>
- replicators
  - <class 'django.db.models.fields.related.ManyToManyField'>
"""


from .schemata import schemata


"""
  parameters:
    pageParam:
      in: query
      name: page
      required: false
      schema:
        type: integer
        minimum: 1
      description: The page number to return.
    itemsPerPageParam:
      in: query
      name: items_per_page
      required: false
      schema:
        type: integer
        minimum: 1
      description: The maximum number of items to return.

"""

OPENAPI_VERSION = '3.0.0'

THIS_API_VERSION = '3.0.0'  # just a coincidence

# These values must be configurable.
THIS_API_TITLE = 'Archivematica Storage Service API'
THIS_API_DESCRIPTION = (
    'An API for the Archivematica Storage Service.')
THIS_API_DFLT_SERVER_DESCRIPTION = (
    'The default server for the Archivematica Storage Service.')

class OpenAPI(object):

    def generate_open_api_yaml(self):
        info = OrderedDict({
            'version': THIS_API_VERSION,
            'title': THIS_API_TITLE,
            'description': THIS_API_DESCRIPTION,
        })

        servers = (
            OrderedDict({
                'url': '/api/{}'.format(self.get_api_version_slug()),
                'description': THIS_API_DFLT_SERVER_DESCRIPTION,
            }),
        )

        security = (
            {'ApiKeyAuth': []},
        )

        components = OrderedDict()

        ApiKeyAuth = OrderedDict()
        ApiKeyAuth['type'] = 'apiKey'
        ApiKeyAuth['in'] = 'header'
        ApiKeyAuth['name'] = 'Authorization'  # value must be ``ApiKey <username>:<api_key>``

        securitySchemes = OrderedDict()
        securitySchemes['ApiKeyAuth'] = ApiKeyAuth

        parameters = OrderedDict()
        for schema in schemata:
            for parameter in schema.extract_parameters():
                parameter_name = '{}_param'.format(parameter['name'])
                parameters[parameter_name] = parameter

        schemas = self.get_schemas()

        components['securitySchemes'] = securitySchemes
        components['parameters'] = parameters
        components['schemas'] = schemas


        ret = OrderedDict()
        ret['openapi'] = OPENAPI_VERSION
        ret['info'] = info
        ret['servers'] = servers
        ret['security'] = security
        ret['components'] = components

        print(json.dumps(ret, indent=4))


    def get_schemas(self):
        schemas = {}
        for resource_name, resource_cfg in self.resources.items():

            read_schema_name = '{}View'.format(resource_name.capitalize())
            read_schema_properties = {}
            read_schema = {'type': 'object'}
            # write_schema_name = '{}Mutate'.format(resource_name.capitalize())
            # write_schema = {}

            resource_cls = resource_cfg['resource_cls']
            model_cls = resource_cls.model_cls
            schema_cls = resource_cls.schema_cls

            print('=' * 80)
            print(read_schema_name)
            # print('\n'.join(dir(model_cls)))
            for field in model_cls._meta.get_fields():
                field_dict = {}
                field_cls_name = field.__class__.__name__
                openapi_type = django_field_class2openapi_type.get(
                    field_cls_name, 'unknown')
                field_dict['type'] = openapi_type
                openapi_format = django_field_class2openapi_format.get(
                    field_cls_name)
                if openapi_format:
                    field_dict['format'] = openapi_format
                read_schema_properties[field.name] = field_dict

                if field_cls_name == 'ForeignKey':
                    to_field_name = field.to_fields[0]
                    to_field = field.related_model._meta.get_field(to_field_name)
                    to_field_cls_name = to_field.__class__.__name__
                    to_field_openapi_type = django_field_class2openapi_type.get(
                        to_field_cls_name, 'unknown')
                    field_dict['type'] = to_field_openapi_type
                    to_field_openapi_format = django_field_class2openapi_format.get(
                        to_field_cls_name)
                    if to_field_openapi_format:
                        field_dict['format'] = to_field_openapi_format
                elif field_cls_name == 'ManyToManyField':
                    to_field_name = field.m2m_target_field_name()
                    to_field = field.related_model._meta.get_field(to_field_name)
                    to_field_cls_name = to_field.__class__.__name__
                    to_field_openapi_type = django_field_class2openapi_type.get(
                        to_field_cls_name, 'unknown')
                    field_dict['type'] = 'array'
                    field_dict['items'] = {'type': to_field_openapi_type}
                    to_field_openapi_format = django_field_class2openapi_format.get(
                        to_field_cls_name)
                    if to_field_openapi_format:
                        field_dict['items']['format'] = to_field_openapi_format
                elif field_cls_name == 'ManyToManyRel':
                    print('{}.{} is a ManyToManyRel'.format(resource_name, field.name))
                    print('\n'.join(dir(field)))
                    related_model = field.related_model
                    print('related_model')
                    print(related_model)
                    print('name')
                    print(field.name)
                    print('field.to')
                    print(field.to)
                    print('END ManyToManyRel')
                elif openapi_type == 'unknown':
                    pass
                    #print('UNKNOWN')
                    #print('- ' + field.name)
                    #print('  - ' + str(type(field)))
                    #print('  - ' + openapi_type)
                    # print('\n'.join(dir(field)))

                #print('- ' + str(field))
                #print('- ' + '\n- '.join(dir(field)))
                #print('\n')

            print('=' * 80)
            read_schema['properties'] = read_schema_properties
            schemas[read_schema_name] = read_schema
        return schemas


    def get_api_version_slug(self):
        return self._get_api_version_slug(THIS_API_VERSION)

    @staticmethod
    def _get_api_version_slug(version):
        """How worky::

            >>> get_api_version_slug('3.0.0')
            ... 'v3'
            >>> get_api_version_slug('3.0.1')
            ... 'v3_0_1'
            >>> get_api_version_slug('3.0')
            ... 'v3'
            >>> get_api_version_slug('3.9')
            ... 'v3_9'
        """
        parts = version.strip().split('.')
        new_parts = []
        for index, part in enumerate(parts):
            part_int = int(part)
            if part_int:
                new_parts.append(part)
            else:
                parts_to_right = parts[index + 1:]
                non_empty_ptr = [p for p in parts_to_right if int(p)]
                if non_empty_ptr:
                    new_parts.append(part)
        return 'v{}'.format('_'.join(new_parts))
