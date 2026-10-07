import os

from flask import Flask, jsonify, request

from app.calculator import add, divide, multiply, subtract

OPERATIONS = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            service="hello-cicd calculator",
            version=os.getenv("APP_VERSION", "dev"),
            operations=sorted(OPERATIONS),
        )

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/calc/<op>")
    def calc(op):
        # APP_API_KEY is injected from a GitHub Actions secret in the CD pipeline.
        # When it is set, every request has to send it in the X-API-Key header.
        api_key = os.getenv("APP_API_KEY")
        if api_key and request.headers.get("X-API-Key") != api_key:
            return jsonify(error="invalid or missing API key"), 401

        if op not in OPERATIONS:
            return jsonify(error=f"unknown operation '{op}'"), 404

        try:
            a = float(request.args["a"])
            b = float(request.args["b"])
        except (KeyError, ValueError):
            return jsonify(error="query parameters a and b must both be numbers"), 400

        try:
            result = OPERATIONS[op](a, b)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400

        return jsonify(op=op, a=a, b=b, result=result)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
