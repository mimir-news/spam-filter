# Standard library
from typing import Any, Dict, List, Optional

# 3rd party modules
from flask import request

# Internal modules
from app.controllers import errors


def get_param(param_name: str) -> str:
    """Gets a required query parameter from a request.

    :param param_name: Name of parameter.
    :return: Value of the prameter as a string
    """
    value = request.args.get(param_name)
    if not value:
        raise errors.BadRequestError(f'Missing required param: {param_name}')
    return value


def get_optional_param(param_name: str, default: str) -> str:
    """Gets an optional query parameter from a request.

    :param param_name: Name of parameter.
    :param default: Default value if not param not found.
    :return: Value of the parameter as a string"""
    value = request.args.get(param_name)
    if not value:
        return default
    return value


def get_json_body(*required_fields: str, fields_as_strings: bool = True) -> Dict[str, Any]:
    """Gets, parses and validated a requests body.

    :param required_fields: Optional list of required field names in the body.
    :param fields_as_strings:
    :return: Request body as a dict.
    """
    body = request.get_json(silent=True)
    if body == None:
        raise errors.BadRequestError('Could not parse request body')
    for field in required_fields:
        if not field in body or body[field] == None:
            raise errors.BadRequestError(f'Missing field: "{field}"')
        if not is_string(body[field]):
            raise errors.BadRequestError(f'"{field}" not of string type')
    return body


def is_string(obj: Any) -> bool:
    """Checks if an object is of type string.

    :param obj: Ojbect to check.
    :return: Boolean
    """
    return isinstance(obj, str)
