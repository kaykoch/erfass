# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#     USER-BEREICH
# ------------------------------------------------------------------------------

import logging

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from markupsafe import Markup
from sqlalchemy.exc import SQLAlchemyError

from src.extensions import state
from src.helpies import _get_klassen_choices

logger = logging.getLogger(__name__)
bp = Blueprint("main", __name__)  # Name und optional url_prefix


def handle_schueler_form(*, schulform_name: str, redirect_endpoint: str) -> Response:
    """Verarbeitet formularbasierte Neuanlage von Schüler-Datensätzen generisch für unterschiedliche Schulformen.

    Die Funktion kapselt den gemeinsamen Ablauf:
    - Formular erstellen und mit dynamischen Klassen-Choices befüllen
    - Validierung und Übernahme der Formulardaten in ein neues Model-Objekt
    - Transaktionales Speichern in der Datenbank (Commit/Rollback)
    - Benutzerfeedback via Flash-Nachrichten
    - PRG-Pattern durch Redirect nach erfolgreichem Speichern
    - Rendering des passenden Templates bei GET oder ungültigem POST

    Args:
        schulform (str): Schlüssel der Schulform (z. B. "berufsschule", "vollzeitschule");
            dient u. a. zur Ermittlung der Klassen-Choices.
        redirect_endpoint (str): Flask-Endpointname, zu dem nach erfolgreichem Speichern per Redirect
            navigiert wird (PRG-Pattern).

    Returns:
        Response: Flask-Response-Objekt.
            - Bei erfolgreichem POST: Redirect auf `redirect_endpoint`
            - Bei GET oder ungültigem POST: Gerenderte HTML-Seite (`template`) mit Formular

    Nebenwirkungen:
        - Schreibt Datensätze in die Datenbank (INSERT) und committet/rollt zurück.
        - Setzt Flash-Nachrichten (success/error).
        - Liest dynamische Klassen-Choices über `_get_klassen_choices(...)`.

    Fehlerbehandlung:
        - Datenbankfehler (SQLAlchemyError) werden geloggt, die Transaktion wird per Rollback zurückgesetzt,
          und es erfolgt eine Fehlermeldung per Flash.
        - Unerwartete Ausnahmen werden geloggt, per Rollback bereinigt und mit einer generischen
          Fehlermeldung quittiert.

    Hinweise:
        - `form_cls` und `model_cls` werden als Klassen (nicht Instanzen) erwartet und in der Funktion
          instanziiert.
        - Die Funktion setzt voraus, dass `SCHULFORMEN[schulform]` für die Klassen-Choices verfügbar ist.
    """
    # Schulform extrahieren
    schulform = state.schulformen.get_schulform(schulform_name)

    # wtf_Form laden
    form = schulform.form_cls()

    # model laden
    model_cls = schulform.model_cls()

    # Templatename bauen
    template = f"{schulform_name}.html"

    # Dropdown-Choices für Klassen dynamisch setzen
    form.klassenbezeichnung.choices = _get_klassen_choices(schulform)

    if form.validate_on_submit():
        try:
            obj = model_cls
            form.populate_obj(obj)

            state.db.session.add(obj)
            state.db.session.commit()

            flash("Schüler erfolgreich gespeichert!", "success")
            # PRG-Pattern
            return redirect(url_for(redirect_endpoint))

        except SQLAlchemyError as e:
            state.db.session.rollback()
            logger.error(f"DB-Fehler in {redirect_endpoint}: {e}", "error")
            flash("Der Eintrag konnte nicht gespeichert werden.", "error")

        except Exception as e:
            state.db.session.rollback()
            logger.error(f"Unerwarteter Fehler in {redirect_endpoint}: {e}")
            flash("Es ist ein unerwarteter Fehler aufgetreten.", "error")

    elif request.method == "POST":
        logger.error(
            f"Formular-Fehler in {redirect_endpoint}: {form.errors}",
        )
        flash("Bitte Eingaben prüfen.", "error")

    return render_template(
        template,
        schulform=schulform_name,
        form=form,
        showAdminMenu=None,
    )


@bp.route("/")
def index():
    schulform = state.schulformen.get_schulform("vollzeitschule")
    form = schulform.form_cls()
    info = "<span class = 'blink'>Zuerst die Schule auswählen</span>"
    flash(Markup(info), "info")
    return render_template("vollzeitschule.html", form=form)


@bp.route("/vollzeitschule.html", methods=["GET", "POST"])
def route_vollzeitschule():
    return handle_schueler_form(
        schulform_name="vollzeitschule",
        redirect_endpoint="main.route_vollzeitschule",
    )


@bp.route("/berufsschule.html", methods=["GET", "POST"])
def route_berufsschule():
    return handle_schueler_form(
        schulform_name="berufsschule",
        redirect_endpoint="main.route_berufsschule",
    )
