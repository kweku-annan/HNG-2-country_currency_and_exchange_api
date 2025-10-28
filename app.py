from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from api.routes.country_routes import country_bp
from api.schemas.dbStorage import DBStorage
from config import Config

# Initialize extensions
# db = SQLAlchemy()
app = Flask(__name__)

# Initialize storage
storage = DBStorage()

# Register blueprints
app.register_blueprint(country_bp)

# def create_app():
#     """Creates and configures the Flask application"""
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     db.init_app(app)
#
#     with app.app_context():
#
#         db.create_all()


@app.route('/', methods=['GET'])
def home():
    return jsonify("Welcome to the Country Currency & Exchange API"), 200

    # return app



if __name__ == "__main__":
    # app = create_app()
    app.run(debug=True)

