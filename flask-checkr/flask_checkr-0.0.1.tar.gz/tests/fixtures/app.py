import json
from flask import Flask, Response, jsonify
from flask_schema import Schema, RequestValidationError, ResponseValidationError

app = Flask('test_app')
schema = Schema()
schema.init_app(app)


@app.errorhandler(RequestValidationError)
def handle_bad_request(e):
    return Response(
        json.dumps(e.to_dict()),
        status=400,
        content_type="application/json",
    )


@app.errorhandler(ResponseValidationError)
def handle_bad_request(e):
    app.logger.exception("response does not match the contract!!! %s", e.to_dict())
    return Response(json.dumps({
        "error": "There was an issue while processing the request. Please try again later.",
        "code": "server_error",
    }), 500, content_type="application/json")


@app.route("/test_get_request_body_validated", methods=["GET"])
def h():
    return jsonify("OK")


@app.route("/test_ok_valid", methods=["POST"])
@schema.check_request("tests/fixtures/definitions/test_ok_valid_req.json")
@schema.check_response("tests/fixtures/definitions/test_ok_valid_res.json")
def ok_valid():
    return jsonify({
        "state": "sent"
    })


@app.route("/test_ok_valid", methods=["POST"])
@schema.check_request("tests/definitions/test_ok_valid_req.json")
@schema.check_response("tests/definitions/test_ok_valid_res.json")
def ok_request_bad():
    return jsonify({"state": "sent"})
