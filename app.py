from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify("Welcome to the Country Currency & Exchange API"), 200


if __name__ == "__main__":
    app.run(debug=True)

