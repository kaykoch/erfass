# -*- coding: utf-8 -*-
import logging

from flask import Flask

from src.config import BaseConfig
from src.extensions import state  # state ist Objekt der Klasse AppState und beinhaltet db)
from src.helpies import _init_db, _update_app

logger = logging.getLogger(__name__)


def create_app(config_object=BaseConfig):
    app = Flask(__name__)

    # Basiskonfiguration laden
    app.config.from_object(config_object)

    # Extensions an App binden (db ist Eigenschaft von state )
    state.db.init_app(app)

    with app.app_context():
        try:
            logger.info(50 * "#")

            # States setzen (Pfade, app, und Schulformen)
            state.set_data(
                app,
                klassenfile="klassen.csv",
                prototype_klassen="prototyp_klassen.csv",
                prototype_bewerber="prototyp_bewerber.xlsx",
            )

            # Wenn die Datenbank nicht existiert, wird sie mit den default Config Werten erstellt
            # state wird als globale Variable in helpies verankert
            _init_db(state)

            # Weitere Configdaten aus der Datenbank laden
            _update_app()

        except Exception as e:
            logger.exception(f"Fehler bei der App-Initialisierung: {e}")

    # Blueprints/Routes registrieren
    from src.routes import bp as main_bp  # nur den Blueprint importieren
    from src.routes_admin import bp as admin_bp  # nur den Blueprint importieren

    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    logger.info("App: Erfassungsbogen wurde erfolgreich gestartet")
    logger.info(50 * "#")

    return app


app = create_app(BaseConfig)
