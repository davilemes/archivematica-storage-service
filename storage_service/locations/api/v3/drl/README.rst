================================================================================
  Storage Service API Version 3
================================================================================

user API::

    import drl
    resources = {
        'location': {
            'resource_class': LocationResource,
            'model_class': Location,
            'schema_class': LocationSchema
        },
        'package': {
            'resource_class': PackageResource,
            'model_class': Package,
            'schema_class': PackageSchema
        },
        'space': {
            'resource_class': SpaceResource,
            'model_class': Space,
            'schema_class': SpaceSchema
        },
        'pipeline': {
            'resource_class': PipelineResource,
            'model_class': Pipeline,
            'schema_class': PipelineSchema
        }
    }
    drl.register_resources(resources)
    urlpatterns = drl.get_urlpatterns()
    openapi_schema = drl.get_openapi_schema()  # a YAML file


Get all resources of a given type
================================================================================

Example: GET /pipelines/::

    $ curl -H "Authorization: ApiKey test:test" \
          http://127.0.0.1:62081/api/v3/pipelines/
    [
        {
            "api_key": "test",
            "uuid": "3bf15d1c-4c7e-4002-b7b0-668983869d49",
            "resource_uri": "/api/v3/pipelines/3bf15d1c-4c7e-4002-b7b0-668983869d49/",
            "enabled": true,
            "api_username": "test",
            "remote_name": "172.20.0.13",
            "id": 1,
            "description": "Archivematica on f5c59e3ed603"
        }
    ]

Pagination works by passing query parameters ``page`` and ``items_per_page``.
Example: GET /locations/ with pagination::

    $ curl -H "Authorization: ApiKey test:test" \
          http://127.0.0.1:62081/api/v3/locations/?page=2&items_per_page=2
    {
        "paginator": {
            "count": 7,
            "items_per_page": 2,
            "page": 2
        },
        "items": [
            {
                "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
                "used": 0,
                "uuid": "5dfd0998-35a6-4724-b428-e538a8f2cdd5",
                "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
                "description": "",
                "enabled": true,
                "quota": null,
                "relative_path": "home",
                "purpose": "TS",
                "replicators": [],
                "id": 1,
                "resource_uri": "/api/v3/locations/5dfd0998-35a6-4724-b428-e538a8f2cdd5/"
            },
            {
                "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
                "used": 0,
                "uuid": "7b1784b1-8887-453e-9be3-087ab2e0bb63",
                "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
                "description": "Default transfer backlog",
                "enabled": true,
                "quota": null,
                "relative_path": "var/archivematica/sharedDirectory/www/AIPsStore/transferBacklog",
                "purpose": "BL",
                "replicators": [],
                "id": 4,
                "resource_uri": "/api/v3/locations/7b1784b1-8887-453e-9be3-087ab2e0bb63/"
            }
        ]
    }


Get a single resource by its UUID
================================================================================

Example: GET /pipelines/<UUID>/::

    $ curl -H "Authorization: ApiKey test:test" \
          http://127.0.0.1:62081/api/v3/pipelines/3bf15d1c-4c7e-4002-b7b0-668983869d49/
    {
        "api_key": "test",
        "uuid": "3bf15d1c-4c7e-4002-b7b0-668983869d49",
        "resource_uri": "/api/v3/pipelines/3bf15d1c-4c7e-4002-b7b0-668983869d49/",
        "enabled": true,
        "api_username": "test",
        "remote_name": "172.20.0.13",
        "id": 1,
        "description": "Archivematica on f5c59e3ed603"
    }


Search across resources
================================================================================

Search works by making a ``SEARCH`` request to the standard collection URI of
the resource (``/resources/``) or a ``POST`` request to ``/resources/search/``,
e.g., ``/locations/search/``.

The request body should contain a object (dict) that has a ``query`` key and an
optional ``paginator`` key. The values of both of these keys are objects. The
``query`` dict has a ``filter`` key and an optional ``order_by`` key. Example::

    {
        "query": {
            "filter": ["Location", "purpose", "regex", "[AT]S"]
            "order_by": [ ... ]
        },
        "paginator": { ... }
    }

Regex search for transfer source and archival storage locations. SEARCH
/locations/::

    $ curl -H "Authorization: ApiKey test:test" \
           -H "Content-Type: application/json" \
           -X SEARCH \
           -d '{"query": {"filter": ["Location", "purpose", "regex", "[AT]S"]}}' \
           http://127.0.0.1:62081/api/v3/locations/
    [
        {
            "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
            "used": 0,
            "uuid": "5dfd0998-35a6-4724-b428-e538a8f2cdd5",
            "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
            "description": "",
            "enabled": true,
            "quota": null,
            "relative_path": "home",
            "purpose": "TS",
            "replicators": [],
            "id": 1,
            "resource_uri": "/api/v3/locations/5dfd0998-35a6-4724-b428-e538a8f2cdd5/"
        },
        {
            "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
            "used": 0,
            "uuid": "a933c327-f081-4faa-b5dc-a0c81f4f494f",
            "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
            "description": "Store AIP in standard Archivematica Directory",
            "enabled": true,
            "quota": null,
            "relative_path": "var/archivematica/sharedDirectory/www/AIPsStore",
            "purpose": "AS",
            "replicators": [],
            "id": 2,
            "resource_uri": "/api/v3/locations/a933c327-f081-4faa-b5dc-a0c81f4f494f/"
        }
    ]

The same search as above, but with reverse ordering and using ``POST
/locations/search/``::

    $ curl -H "Authorization: ApiKey test:test" \
           -H "Content-Type: application/json" \
           -X POST \
           -d '{"query": {"filter": ["Location", "purpose", "regex", "[AT]S"], "order_by": [["purpose"]]}}' \
           http://127.0.0.1:62081/api/v3/locations/search/
    [
        {
            "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49" ],
            "used": 0,
            "uuid": "a933c327-f081-4faa-b5dc-a0c81f4f494f",
            "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
            "description": "Store AIP in standard Archivematica Directory",
            "enabled": true,
            "quota": null,
            "relative_path": "var/archivematica/sharedDirectory/www/AIPsStore",
            "purpose": "AS",
            "replicators": [],
            "id": 2,
            "resource_uri": "/api/v3/locations/a933c327-f081-4faa-b5dc-a0c81f4f494f/"
        },
        {
            "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
            "used": 0,
            "uuid": "5dfd0998-35a6-4724-b428-e538a8f2cdd5",
            "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
            "description": "",
            "enabled": true,
            "quota": null,
            "relative_path": "home",
            "purpose": "TS",
            "replicators": [],
            "id": 1,
            "resource_uri": "/api/v3/locations/5dfd0998-35a6-4724-b428-e538a8f2cdd5/"
        }
    ]

The same search as above, this time adding pagination::

    $ curl -H "Authorization: ApiKey test:test" \
           -H "Content-Type: application/json" \
           -X POST \
           -d '{"paginator": {"page": 2, "items_per_page": 1}, "query": {"filter": ["Location", "purpose", "regex", "[AT]S"], "order_by": [["purpose"]]}}' \
           http://127.0.0.1:62081/api/v3/locations/search/
    {
        "paginator": {
            "count": 2,
            "items_per_page": 1,
            "page": 2
        },
        "items": [
            {
                "pipeline": ["3bf15d1c-4c7e-4002-b7b0-668983869d49"],
                "used": 0,
                "uuid": "5dfd0998-35a6-4724-b428-e538a8f2cdd5",
                "space": "c7463e9b-88d2-4674-a85b-5fc6905fd233",
                "description": "",
                "enabled": true,
                "quota": null,
                "relative_path": "home",
                "purpose": "TS",
                "replicators": [],
                "id": 1,
                "resource_uri": "/api/v3/locations/5dfd0998-35a6-4724-b428-e538a8f2cdd5/"
            }
        ]
    }
