from marshmallow import Schema, fields
from flask import make_response
from flask_sqlalchemy import Pagination

STATUS_COLLECTION = {
    200: "200 OK",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    409: "409 Resource Exist",
    422: "422 Unprocessable Entity",
    500: "500 Internal Server Error",
}


class PaginateSchema(Schema):
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    page = fields.Integer()
    pages = fields.Integer()
    total = fields.Integer()

    class Meta:
        fields = ("has_next", "has_prev", "page", "pages", "total")


def json_response(data=None, message="ok", status=200, paginate=None, data_status=None):
    body = {
        "data": data,
        "message": message
    }
    if data_status:
        body["status"] = data_status
    if paginate and isinstance(paginate, Pagination):
        paginate_schema = PaginateSchema()
        body["paginate"] = paginate_schema.dump(paginate).data

    response = make_response(body)

    assert status in STATUS_COLLECTION
    response.status = STATUS_COLLECTION[status]
    return response
