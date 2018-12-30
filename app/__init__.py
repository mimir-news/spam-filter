# Standard library
import logging
from datetime import datetime
from typing import Optional
from uuid import uuid4

# 3rd party modules.
import flask
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

# Internal modules
from app.config import AppConfig
from app.config import REQUEST_ID_HEADER, SERVICE_NAME, SERVER_NAME

app = Flask(SERVICE_NAME)
app.config.from_object(AppConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app)


from app import routes, models
from app.controllers import errors


error_log = logging.getLogger('ErrorHandler')


@app.before_request
def add_request_id() -> None:
    """Adds a request id to an incomming request."""
    incomming_id: Optional[str] = request.headers.get(REQUEST_ID_HEADER)
    request.id = incomming_id if incomming_id != None else str(uuid4())


@app.after_request
def add_request_id_to_response(response: flask.Response) -> flask.Response:
    """Adds request id header to each response.

    :param response: Response to add header to.
    :return: Response with header.
    """
    response.headers[REQUEST_ID_HEADER] = request.id
    response.headers["Server"] = SERVER_NAME
    response.headers["Date"] = f"{datetime.utcnow()}"
    return response


@app.errorhandler(errors.RequestError)
def handle_request_error(error: errors.RequestError) -> flask.Response:
    """Handles errors encountered when handling requests.

    :param error: Encountered RequestError.
    :return: flask.Response indicating the encountered error.
    """
    if error.status() >= 500:
        error_log.error(str(error))
    else:
        error_log.warning(str(error))
    json_error = jsonify(error.asdict())
    return make_response(json_error, error.status())
