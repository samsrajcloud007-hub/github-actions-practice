from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(message="Welcome to the CI Practice Flask App!")


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/api/greet/<name>")
def greet(name):
    if not name.strip():
        return jsonify(error="Name cannot be empty"), 400
    return jsonify(message=f"Hello, {name}!")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    operation = data.get("operation")
    a = data.get("a")
    b = data.get("b")

    if operation not in {"add", "subtract", "multiply", "divide"}:
        return jsonify(error="Invalid or missing operation"), 400

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify(error="'a' and 'b' must be numbers"), 400

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    else:  # divide
        if b == 0:
            return jsonify(error="Cannot divide by zero"), 400
        result = a / b

    return jsonify(operation=operation, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(debug=True)
