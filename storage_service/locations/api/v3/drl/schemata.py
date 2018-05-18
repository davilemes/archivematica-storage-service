from collections import OrderedDict

from formencode.schema import Schema
from formencode.validators import Int

formencode_cls2openapi_type = {
    'Int': 'integer',
}


class OpenAPISchema(object):

    def __init__(self, formencode_schema, config):
        self.formencode_schema = formencode_schema
        self.config = config

    # P.fields
    # {'items_per_page': <Int object 64 min=1 not_empty=True>,
    #  'page': <Int object 65 min=1 not_empty=True>}
    def extract_parameters(self):
        parameters = []
        for parameter_name, formencode_cls in self.formencode_schema.fields.items():
            config = self.config.get(parameter_name, {})
            parameter = OrderedDict()
            schema = OrderedDict()

            parameter['in'] = config.get('in', 'query')
            parameter['name'] = parameter_name
            parameter['required'] = config.get(
                'required', formencode_cls.not_empty)

            schema['type'] = formencode_cls2openapi_type.get(
                formencode_cls, 'string')

            minimum = formencode_cls.min
            if minimum is not None:
                schema['minimum'] = minimum

            parameter['schema'] = schema

            description = config.get('description', None)
            if description is not None:
                parameter['description'] = description

            parameters.append(parameter)
        return parameters


class PaginatorSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = False
    items_per_page = Int(not_empty=True, min=1)
    page = Int(not_empty=True, min=1)


PaginatorOpenAPISchema = OpenAPISchema(
    PaginatorSchema,
    {
        'page': {
            'description': 'The page number to return.'
        },
        'items_per_page': {
            'description': 'The maximum number of items to return.'
        }
    })

schemata = (PaginatorOpenAPISchema,)

__all__ = ('schemata', 'PaginatorSchema')
