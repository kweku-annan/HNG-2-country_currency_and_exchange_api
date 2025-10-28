from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions
db = SQLAlchemy()


def create_app():
    """Creates and configures the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from api.models.countries import Country
        db.create_all()


    @app.route('/', methods=['GET'])
    def home():
        return jsonify("Welcome to the Country Currency & Exchange API"), 200

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

