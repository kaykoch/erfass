import logging
from typing import Dict, List, Tuple, Type

from src.extensions import db
from src.forms import BerufsschuelerForm, VollzeitschuelerForm
from src.helpies import _import_klassen_from_csv

logger = logging.getLogger(__name__)

MAX_EXPORT_ROWS = 1000


# Daten, wie Adminpassword. -login, Mailzugang
class ConfigSetting(db.Model):
    __tablename__ = "ConfigSetting"

    id = db.Column(db.Integer, primary_key=True)

    # Admin Credentials
    admin_login = db.Column(db.String(100), nullable=False, default="admin")
    admin_password = db.Column(db.String(255), nullable=False, default="admin")

    # Mail Server Einstellungen
    mail_server = db.Column(db.String(255), default="imap.beatles.com")
    mail_port = db.Column(db.Integer, default=587)
    mail_use_tls = db.Column(db.Boolean, default=False)
    mail_use_ssl = db.Column(db.Boolean, default=True)
    mail_username = db.Column(db.String(255), default="john@beatles.com")
    mail_password = db.Column(db.String(255), default="yellosubmarine")
    mail_default_sender = db.Column(db.String(255), default="paul@beatles.com")


# Tabelle 0: Gemeinsame Daten der Schüler
class SchuelerBase(db.Model):
    __abstract__ = True  # Verhindert, dass eine eigene Tabelle für die Basisklasse erstellt wird
    id = db.Column(db.Integer, primary_key=True)

    # Stammdaten
    klassenbezeichnung = db.Column(db.String(50))

    eintrittsdatum = db.Column(db.Date)
    schueler_familienname = db.Column(db.String(100))
    schueler_vorname = db.Column(db.String(100))
    schueler_geburtsdatum = db.Column(db.Date)
    schueler_geburtsort = db.Column(db.String(100))
    schueler_geburtsland = db.Column(db.String(100))
    schueler_geschlecht = db.Column(db.Enum("M", "W", "D", "O", name="geschlecht_types"))
    schueler_staatsangehörigkeit = db.Column(db.String(100))
    schueler_familiensprache = db.Column(db.String(100))
    schueler_strasse = db.Column(db.String(200))
    schueler_hausnummer = db.Column(db.String(50))
    schueler_stadtteil = db.Column(db.String(50))
    schueler_PLZ = db.Column(db.String(10))
    schueler_religion = db.Column(db.String(100))
    schueler_religion_teilnahme = db.Column(db.String(100), server_default="RK")
    schueler_wohnort = db.Column(db.String(100))
    schueler_telefon_1 = db.Column(db.String(30))
    schueler_telefon_2 = db.Column(db.String(30))
    schueler_email = db.Column(db.String(100))

    # Erziehungsberechtigte
    erziehungsberechtigte_1_name = db.Column(db.String(100))
    erziehungsberechtigte_1_vorname = db.Column(db.String(100))
    erziehungsberechtigte_1_PLZ = db.Column(db.String(10))
    erziehungsberechtigte_1_wohnort = db.Column(db.String(100))
    erziehungsberechtigte_1_stadtteil = db.Column(db.String(50))
    erziehungsberechtigte_1_strasse = db.Column(db.String(200))
    erziehungsberechtigte_1_hausnummer = db.Column(db.String(50))
    erziehungsberechtigte_1_telefon_1 = db.Column(db.String(30))
    erziehungsberechtigte_1_telefon_2 = db.Column(db.String(30))
    erziehungsberechtigte_1_email = db.Column(db.String(100))
    erziehungsberechtigte_1_art = db.Column(db.String(30))

    erziehungsberechtigte_2_name = db.Column(db.String(100))
    erziehungsberechtigte_2_vorname = db.Column(db.String(100))
    erziehungsberechtigte_2_PLZ = db.Column(db.String(10))
    erziehungsberechtigte_2_wohnort = db.Column(db.String(100))
    erziehungsberechtigte_2_stadtteil = db.Column(db.String(50))
    erziehungsberechtigte_2_strasse = db.Column(db.String(200))
    erziehungsberechtigte_2_hausnummer = db.Column(db.String(50))
    erziehungsberechtigte_2_telefon_1 = db.Column(db.String(30))
    erziehungsberechtigte_2_telefon_2 = db.Column(db.String(30))
    erziehungsberechtigte_2_email = db.Column(db.String(100))
    erziehungsberechtigte_2_art = db.Column(db.String(30))

    # Schulhistorie
    grundschule_datum = db.Column(db.Date)
    letzte_schule_name = db.Column(db.String(200))
    letzte_schule_ort = db.Column(db.String(100))
    letzte_schule_schulart = db.Column(db.String(100))
    letzte_schule_klasse = db.Column(db.String(20))
    letzte_schule_abschluss = db.Column(db.String(100))
    letzte_schule_abgangsdatum = db.Column(db.Date)
    abschluss_maximal = db.Column(db.String(100))

    # Zusatzangaben

    auslaender_foerderbedarf_deutsch = db.Column(db.Boolean, default=False)
    auslaender_einreisedatum = db.Column(db.Date)


# Tabelle 1: Vollzeit Schüler
class Vollzeitschueler(SchuelerBase):
    __tablename__ = "vollzeitschueler"

    @staticmethod
    def get_name():
        return "vollzeitschule"

    @staticmethod
    def get_form():
        return VollzeitschuelerForm

    def __repr__(self):
        return f"<Vollzeitschueler: {self.schueler_familienname}, {self.schueler_vorname}>"


# Tabelle 2: Schüler in Ausbildung (enthält alle Felder + Betriebsinfos)
class Berufsschueler(SchuelerBase):
    __tablename__ = "berufsschueler"

    @staticmethod
    def get_name():
        return "berufsschule"

    @staticmethod
    def get_form():
        return BerufsschuelerForm

    betrieb_name = db.Column(db.String(200))
    betrieb_anprechpartner_name = db.Column(db.String(100))
    betrieb_anprechpartner_vorname = db.Column(db.String(100))

    betrieb_PLZ = db.Column(db.String(10))
    betrieb_ort = db.Column(db.String(100))
    betrieb_strasse = db.Column(db.String(200))
    betrieb_telefon = db.Column(db.String(30))
    betrieb_email = db.Column(db.String(100))

    ausbildung_beruf = db.Column(db.String(100))
    ausbildung_start = db.Column(db.Date)
    ausbildung_ende = db.Column(db.Date)
    ausbildung_kammer = db.Column(db.Enum("HWK", "IHK", name="kammer_types"))

    def __repr__(self):
        return f"<Berufsschueler: {self.schueler_familienname}, {self.schueler_vorname}>"


# Sammlung aller Schulformen
class Schulformen:
    SCHULFORMEN: Dict[str, "Schulform"] = {}
    KLASSENFILE: str = ""
    ART_MAPPING = {
        "berufsschule": "T",
        "vollzeitschule": "V",
    }

    @classmethod
    def add_schulformen(cls, klassenfile: str, list_model_cls: List[Type]) -> None:
        """Erstellt eine Liste mit Objekten der Klasse Schulform

        Args:
            klassenfile (str): Pfad zur Datei mit den Klassennamen
            list_model_cls (list): Liste der Models der Schulformen
        """
        cls.KLASSENFILE = klassenfile
        for model_cls in list_model_cls:
            # neue Schulform erstellen und ...
            schulform = Schulform(model_cls)
            # ... in die Liste aufnehmen
            cls.SCHULFORMEN[schulform.key] = schulform
            logger.info(f"Schulform: {schulform.display_name} geladen")

        # Klassennamen aus CSV-Datei einlesen
        cls.update_klassen()

    @classmethod
    def get_schulform(cls, schulform_name):
        """liefert das Objekt, dass zum Namen passt

        Args:
            schulform_name (str): Name der Schulform

        Returns:
            _type_: Objekt der Klasse Schulform
        """
        return cls.SCHULFORMEN.get(schulform_name or "")

    @classmethod
    def update_klassen(cls):
        """liest alle Klassen aus der CSV-Datei ein und speichert sie im passenden Objekt"""
        # Alle Klassen aus der CSV holen
        try:
            alle_klassen: List[Tuple[str, str, str]] = _import_klassen_from_csv(cls.KLASSENFILE)
            logger.info(f"{len(alle_klassen)} Schulklassen aus CSV geladen.")

        except Exception as e:
            logger.error(f"Klassenliste konnte nicht geladen werden (pfad={cls.KLASSENFILE}): {e}")
            for meta in cls.SCHULFORMEN.values():
                meta.liste = []
            return

        for key, meta in cls.SCHULFORMEN.items():
            art_code = cls.ART_MAPPING.get(key)  # kann None sein, wenn nicht definiert

            try:
                # Filter nach Art, falls ein Code definiert ist
                if art_code:
                    gefiltert = [(k, b) for k, b, a in alle_klassen if a == art_code]
                else:
                    # Keine Filterung – alle Einträge übernehmen
                    gefiltert = [(k, b) for k, b, _ in alle_klassen]

                # Alphabetisch nach Kurzform sortieren
                gefiltert.sort(key=lambda tup: tup[0])

                meta.liste = gefiltert if isinstance(gefiltert, list) else list(gefiltert or [])

            except Exception as e:
                # Fehler intern loggen, aber nicht die gesamte Aktualisierung abbrechen
                try:
                    logger.error(f"Fehler beim Einlesen der Klassen für '{key}' (pfad={cls.KLASSENFILE}): {e}")
                except Exception:
                    pass
                meta.liste = []

    def __repr__(cls):
        return f"<schulformen: {list(cls.SCHULFORMEN.keys())}>"


# Eine Schulform mit Namen, model, form und Klassenliste
class Schulform:
    """repräsentiert eine Schulform mit Model, Form und Liste aller Klassennamen"""

    def __init__(self, model_cls):
        """Konstruktor

        Args:
            model_cls (_type_): Model der Schulform
        """
        self.model_cls = model_cls  # model
        self.form_cls = model_cls.get_form()  # Form
        self.schulform_name = (model_cls.get_name() or "").strip()  # Name
        self.display_name = self.schulform_name.capitalize()  # Name zur Darstellung
        self.key = self.schulform_name.lower()  # Schlüssel in der Liste
        self.liste: List[Tuple[str, str]] = []  # Liste mit Klassennamen

    def __repr__(self):
        return f"<Schulform: {self.display_name}>"


def update():
    pass
