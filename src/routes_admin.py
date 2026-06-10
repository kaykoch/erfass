# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#     ADMIN-BEREICH
# ------------------------------------------------------------------------------

import logging
import os
from io import BytesIO

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from markupsafe import Markup
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import RequestEntityTooLarge

from src.extensions import state
from src.forms import ConfigForm, FileuploadForm, SchuelerAuswahlForm
from src.helpies import (
    _export_to_csv,
    _export_to_pdf,
    _export_to_xlsx,
    _get_error_page,
    _get_klassen_choices,
    _get_schueler_list,
    _has_same_header,
    _requires_auth,
    _save_file,
)
from src.models import ConfigSetting, Schulformen

logger = logging.getLogger(__name__)
bp = Blueprint("admin", __name__)


@bp.route("/", methods=["GET", "POST"])
@_requires_auth
def route_admin() -> str:
    """zeigt alle administrativen Aufgaben auf einer Webseite"""
    title = "Administration - Ausbilderbetriebe WebUntis"
    info = (
        "<p>Hier finden Sie Links zu allen administrativen Aufgaben:</p>"
        "<p>Eine Dokumentation finden Sie (irgendwann mal) <a href='/static/Dokumentation.pdf' target='_blank'>HIER</a></p>"
    )
    flash(Markup(info), "success")
    return render_template("admin.html", title=title, showAdminMenu=None)


@bp.route("/api/zugeordete_schueler/<schulform_name>/<klasse>")
@_requires_auth
def zugeordete_schueler(schulform_name, klasse):
    """Diese Route wird von JavaScript aufgerufen, um alle Azubis einer Klasse anzuzeigen."""
    try:
        # Validierung der Schulform (Whitelist)
        if schulform_name not in Schulformen.SCHULFORMEN:
            return jsonify(list())

        model_cls = Schulformen.get_schulform(schulform_name).model_cls
        if model_cls is None:
            return jsonify(list())

        schueler_liste = _get_schueler_list(state.db, model_cls, klasse)
        # Als JSON zurückgeben (das versteht JavaScript am besten)
        return jsonify(schueler_liste)

    except Exception as e:
        logger.error(f"Fehler in zugeordete_schueler(schulform={schulform_name}, klasse={klasse}): {e}")
        return jsonify(list())


@bp.route("/schueleranzeige.html", methods=["GET", "POST"])
@_requires_auth
def route_schueleranzeige() -> str:
    """Anzeige und Download der Schüler einer einzelnen Klasse oder aller Schueler.

    Returns:
        str: Webseite
    """
    title = "Anzeige und Download der Azubis"
    try:
        # Daten aus GET oder POST holen
        schulform_name = request.values.get("schulform")
        if schulform_name not in state.schulformen.SCHULFORMEN:
            # Erster Eintrag als Default
            schulform_name = next(iter(state.schulformen.SCHULFORMEN))

        # Das Model mit den gewünschen Schülern laden
        model_cls = Schulformen.get_schulform(schulform_name).model_cls
        # Liste der möglichen Klassennamen von Schülern aus diesem Model extrahieren
        stmt = (
            state.db.select(model_cls.klassenbezeichnung)
            .distinct()
            .order_by(
                model_cls.klassenbezeichnung.asc(),
            )
        )
        klassen_liste = state.db.session.execute(stmt).scalars().all()

        form = SchuelerAuswahlForm()
        # Choices dynamisch zusammenbauen mit Klassennamen
        form.klassen.choices = [("", "Bitte wählen..."), ("all", "Alle Klassen")] + [(k, k) for k in klassen_liste if k]

        # Daten überprüfen, wenn der Download-Button gedrückt wurde
        if form.validate_on_submit():
            # Aktuelle Klasse auslesen
            klasse = form.klassen.data
            # Wenn Klasse nicht in klassen_liste ist, oder leer ist -> default="all"
            if klasse not in klassen_liste:
                klasse = "all"

            # Aktuelle Schulform auslesen
            schulform_name = form.schulform.data

            # Schüler der Schulform und Klasse laden (max. 500 Einträge)
            schueler_liste = _get_schueler_list(state.db, model_cls, klasse)
            print(1, schueler_liste)

            export_configs = {
                "submit_csv": {
                    "exporter": lambda: _export_to_csv(schueler_liste),
                    "mimetype": "text/csv; charset='utf-8'",
                    "ext": "csv",
                },
                "submit_xlsx": {
                    "exporter": lambda: _export_to_xlsx(schueler_liste, state.prototype_bewerber),
                    "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "ext": "xlsx",
                },
                "submit_pdf": {
                    "exporter": lambda: _export_to_pdf(schueler_liste, schulform_name, klasse),
                    "mimetype": "application/pdf",
                    "ext": "pdf",
                },
            }
            # Auswahl der Aktion
            # 2. Dynamisch prüfen, welcher Button gedrückt wurde
            for test_name, config in export_configs.items():
                # ist tatsächlich test_name der gedrückte button?
                button = getattr(form, test_name, None)
                if button and button.data:
                    # Export-Funktion ausführen
                    file_io = config["exporter"]()

                    # Datei senden
                    return send_file(
                        file_io,
                        mimetype=config["mimetype"],
                        as_attachment=True,
                        download_name=f"export.{config['ext']}",
                        conditional=False,
                    )

            else:
                # Keine erkannte Aktion
                return "Aktion nicht gefunden", 404

        elif request.method == "POST":
            logger.error("Formular-Fehler im Modul schueleranzeige:", form.errors)

        info = (
            "Nach der Auswahl einer Klasse werden alle Azubis sortiert nach Klasse und Nachname angezeigt.<br>"
            "Durch Klick auf die ID kann der Schüler bearbeitet oder die angezeigten Schüler als CSV- "
            "oder PDF-Datei heruntergeladen werden."
        )
        flash(Markup(info), "success")

        return render_template(
            "schueleranzeige.html",
            title=title,
            schulform=schulform_name,
            form=form,
            showAdminMenu=True,
        )

    except Exception as e:
        logger.error(f"Fehler im Modul route_schueleranzeige: {e}")
        return _get_error_page()


@bp.route("/upload.html", methods=["GET", "POST"])
@_requires_auth
def route_upload() -> str:
    """Bietet die Möglichkeit die Datei mit den neuen Klassennamen zu importieren
    Der Header der Datei wird mit dem des Prototypen verglichen
    Returns:
        str: Webseite
    """
    title = "Upload Klassenliste - WebUntis"
    confirmmsg = "Möchtest du wirklich die bisherige Datei überschreiben?"

    try:
        form = FileuploadForm()

        if form.validate_on_submit():
            # Header verleichen
            file_storage = form.upload_file.data
            stream = BytesIO(file_storage.read())
            if _has_same_header(stream, state.prototype_klassen):
                # Stream wieder zurück setzen
                file_storage.seek(0)
                # Datei unter dem entsprechenden Pfad speichern
                answer, category = _save_file(file_storage, state.klassenfile)

                # Liste der Klassen neu aus Dateien einlesen
                if category == "success":
                    state.schulformen.update_klassen()

                flash(answer, category)
            else:
                info = (
                    f"Die Datei '{form.upload_file.data.filename}' hat nicht den notwendigen Aufbau.<br>"
                    "Bitte mit dem Prototyp vergleichen"
                )

                flash(Markup(info), "error")

            # PRG-Pattern gegen Doppelklick/Reload
            return redirect(url_for("admin.route_upload"))

        # POST aber ungültig → Fehler anzeigen
        if request.method == "POST":
            logger.error(f"Formular-Fehler im Modul upload: {form.errors}")
            flash(f"Ungültige Eingaben  oder Sitzung abgelaufen. {form.errors}", "error")

        # GET oder ungültiger POST → Hinweis anzeigen
        flash("WICHTIG: Die bisherige Datei mit Daten wird überschrieben.", "warning")
        return render_template(
            "upload.html",
            title=title,
            confirmmsg=confirmmsg,
            form=form,
        )

        return _get_error_page("Die Seite wurde nicht korrekt aufgerufen")

    except RequestEntityTooLarge:
        flash("Dateigröße zu groß.", "warning")
        return redirect(url_for("adin.route_upload"))

    except Exception as e:
        logger.error(f"Fehler im Modul route_upload: {e}")
        return _get_error_page()


@bp.route("/download_prototyp", methods=["GET"])
@_requires_auth
def route_download_prototyp():
    try:
        # Attachment-Name setzen (falls state.prototype_klassen ein Pfad ist)
        filename = os.path.basename(state.prototype_klassen)
        return send_file(
            state.prototype_klassen,
            as_attachment=True,
            download_name=filename,  # Flask ≥ 2.0
            conditional=True,  # ETag/Range unterstützen
        )
    except FileNotFoundError:
        return "Datei nicht gefunden", 404
    except Exception as e:
        logger.error(f"Fehler beim Download des Prototyps: {e}")
        return _get_error_page()


@bp.route("/export_pdf/<schulform>")
@_requires_auth
def route_export_pdf(schulform):
    try:
        if schulform not in Schulformen:
            return "Schulform nicht gefunden", 404

        model_cls = Schulformen.get_schulform(schulform).model_cls
        schueler_liste = _get_schueler_list(state.db, model_cls, "all")
        return _export_to_pdf(schueler_liste, schulform)

    except Exception as e:
        logger.error(f"Fehler in route_export_pdf({schulform}): {e}")
        return _get_error_page()


@bp.route("/update_schueler/<int:id>", methods=["GET", "POST"])
@_requires_auth
def route_updateschueler(id):

    schulform_name = request.values.get("schulform")
    action = request.args.get("action")
    Schulform = Schulformen.get_schulform(schulform_name)
    model_cls = Schulform.model_cls

    schueler = None
    # nur erlaubte actions akzeptieren
    if action in ("next", "back"):
        # Klasse des aktuellen Schülers einmalig lesen
        stmt = state.db.select(model_cls.klassenbezeichnung).where(model_cls.id == id)
        klasse = state.db.session.execute(stmt).scalar_one_or_none()

        if klasse is not None:
            # Basisfilter: gleiche Klasse
            filters = [model_cls.klassenbezeichnung == klasse]

            # Richtung und Reihenfolge bestimmen
            if action == "next":
                # Nächster Schüler
                filters.append(model_cls.id > id)
                order = asc(model_cls.id)
            else:
                # vorheriger Schüler
                filters.append(model_cls.id < id)
                order = desc(model_cls.id)

            stmt = state.db.select(model_cls).where(*filters).order_by(order)
            schueler = state.db.session.execute(stmt).scalars().first()

    # Fallback: aktueller Schüler (oder falls Action fehlte / Klasse nicht gefunden)
    if schueler is None:
        stmt = state.db.select(model_cls).where(model_cls.id == id)
        schueler = state.db.session.execute(stmt).scalars().first()

    # Formular mit Daten des Ausbilders vorbefüllen, falls vorhanden
    form = Schulform.form_cls(obj=schueler)

    form.klassenbezeichnung.choices = _get_klassen_choices(Schulform)

    if form.validate_on_submit():
        form.populate_obj(schueler)

        state.db.session.commit()
        flash("Azubi erfolgreich gespeichert!")
        return redirect(
            url_for(
                "admin.route_updateschueler",
                id=schueler.id,
                schueler=schueler,
                schulform=schulform_name,
            )
        )

    elif request.method == "POST":
        logger.error("Formular-Fehler im Modul route-berufsschueler:", form.errors)

    return render_template(
        f"{schulform_name}.html",
        schulform=schulform_name,
        form=form,
        schueler=schueler,
        showAdminMenu=True,
    )


@bp.route("/config.html", methods=["GET", "POST"])
@_requires_auth
def route_config() -> str:
    """Zeigt die Webseite zur Eingabe der Konfigurtionsdaten an

    Returns:
        str: Webseite
    """
    title = "Einstellungen - Ausbilderbetriebe WebUntis"
    # Konfiguration laden (ersten Datensatz)
    stmt = state.db.select(ConfigSetting).limit(1)
    cfg = state.db.session.execute(stmt).scalar_one_or_none()

    try:
        form = ConfigForm(obj=cfg)
        if form.validate_on_submit():
            # Neu anlegen, falls noch keine Config vorhanden
            if cfg is None:
                cfg = ConfigSetting()
                state.db.session.add(cfg)

            # 1. Alle Felder außer Passwörter automatisch füllen
            # Dazu kopieren wir die Daten, aber lassen die PW-Felder aus
            for fieldname, value in form.data.items():
                if fieldname not in ["admin_password", "mail_password", "csrf_token", "submit"]:
                    setattr(cfg, fieldname, value)

            # 2) Passwörter nur setzen, wenn eingegeben
            if form.admin_password.data:
                cfg.admin_password = form.admin_password.data  # TODO: ggf. hashen
            if form.mail_password.data:
                cfg.mail_password = form.mail_password.data  # TODO: ggf. verschlüsseln

            try:
                # Daten in DB eintragen
                state.db.session.commit()
                flash("Konfiguration erfolgreich gespeichert.", "success")

            except SQLAlchemyError:
                state.db.session.rollback()
                current_app.logger.exception("DB-Fehler beim Speichern der Config")
                flash("Datenbankfehler beim Speichern der Konfiguration.", "error")
                return render_template("config.html", title=title, form=form), 500

        elif request.method == "POST":
            logger.error(f"route_config -> Formular-Fehler im Modul : {form.errors}")

        return render_template(
            "config.html",
            title=title,
            form=form,
        )

    except Exception as e:
        current_app.logger.exception("Fehler im Modul config")
        logger.error(f"Fehler im Modul config: {e}")
        return _get_error_page()
