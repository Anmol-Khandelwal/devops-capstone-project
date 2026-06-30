from flask import jsonify, request, url_for, abort
from service.models import Account
from service import app


@app.route("/health")
def health():
    return jsonify(status="OK"), 200


@app.route("/")
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
    ), 200


@app.route("/accounts", methods=["POST"])
def create_accounts():
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("read_accounts", account_id=account.id, _external=True)
    return jsonify(message), 201, {"Location": location_url}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    return jsonify(account_list), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.id = account_id
    account.update()
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204


def check_content_type(content_type):
    if "Content-Type" not in request.headers:
        abort(415, f"Content-Type must be {content_type}")
    if request.headers["Content-Type"] == content_type:
        return
    abort(415, f"Content-Type must be {content_type}")
