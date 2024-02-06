import logging
from os import getenv
from pathlib import Path
from typing import Final
from dotenv import load_dotenv
from flask import Flask
from app.web.routes.parcel_locker import configure_routes, parcel_lockers_bp


def create_app() -> Flask:
    """
    Function creates Flask app and configures it
    """
    app = Flask(__name__)

    with app.app_context():

        # -------------------------------------------------------------------------------------
        # LOGGER CONFIGURATION
        # -------------------------------------------------------------------------------------
        logging.basicConfig(level=logging.INFO)

        # -------------------------------------------------------------------------------------
        # ENVIRONMENT VARIABLES CONFIGURATION
        # -------------------------------------------------------------------------------------
        ENV_FILENAME: Final = '.env'
        ENV_PATH = Path.cwd().absolute().joinpath(ENV_FILENAME)
        load_dotenv(ENV_PATH)

        # # -------------------------------------------------------------------------------------
        # # DATABASE CONFIGURATION
        # # -------------------------------------------------------------------------------------
        db_username = getenv('USER')
        db_password = getenv('PASSWORD')
        db_port = getenv('PORT', 3306)
        db_name = getenv('DATABASE', 'db_1')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_username}:{db_password}@mysql:{db_port}/{db_name}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # -------------------------------------------------------------------------------------
        # GLOBAL ERROR HANDLER CONFIGURATION
        # -------------------------------------------------------------------------------------
        @app.errorhandler(Exception)
        def all_exception_handler(error):
            error_message = str(error.args)
            return {'error_message': error_message}, 500

        logging.info('APP IS RUNNING')
        
        # -------------------------------------------------------------------------------------
        # ROUTES CONFIGURATION
        # -------------------------------------------------------------------------------------
        configure_routes(app)

        # ----------------------------------------------------------------------
        # BLUEPRINTS CONFIGURATION
        # ----------------------------------------------------------------------
        app.register_blueprint(parcel_lockers_bp)

        return app
