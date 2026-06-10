from __future__ import annotations

import logging
from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    BooleanField,
    DateField,
    EmailField,
    FileField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

logger = logging.getLogger(__name__)


def schueler_geburtsdatum() -> date:
    """Geburtsdatum: 1. August vor 17 Jahren"""
    today = date.today()
    return date(today.year - 17, 1, 1)


def schueler_grundschuldatum() -> date:
    """Grundschuldatum: 1. August Schüler Geburtsjahr + 6 Jahren"""
    return date(schueler_geburtsdatum().year + 6, 8, 1)


def bbs_eintrittsdatum() -> date:
    """BBS Eintrittsdatum: 1. August in diesem Jahr"""
    today = date.today()
    return date(today.year, 8, 1)


# ------------------------------------------------------------------------------
# Config
# ------------------------------------------------------------------------------
class ConfigForm(FlaskForm):
    # Admin
    admin_login = StringField(
        "Admin Login",
        validators=[DataRequired(), Length(max=150)],
    )
    admin_password = PasswordField(
        "Admin Passwort",
        validators=[Optional()],
    )

    # Mail
    mail_server = StringField("Mail Server", validators=[Optional(), Length(max=255)])
    mail_port = IntegerField("Mail Port", validators=[Optional(), NumberRange(min=1, max=65535)])
    mail_use_ssl = BooleanField("Nutze SSL", validators=[Optional()])
    mail_use_tls = BooleanField("Nutze TLS", validators=[Optional()])
    mail_username = StringField("Mail Benutzername", validators=[Optional(), Length(max=255)])
    mail_password = PasswordField("Mail Passwort", validators=[Optional()])
    mail_default_sender = StringField("Standard Absender (E-Mail)", validators=[Optional(), Length(max=320)])

    submit = SubmitField("Einstellungen speichern")


# ------------------------------------------------------------------------------
# Schüler
# ------------------------------------------------------------------------------
class SchuelerBaseForm(FlaskForm):
    """Basisklasse für gemeinsame Schülerfelder (Stammdaten, Historie, Zusatz)."""

    # Deterministische Reihenfolge der Auswahl
    RELIGION_CHOICES = [
        ("RK", "römisch-katholisch"),
        ("EV", "evangelisch"),
        ("JU", "jüdisch"),
        ("ISL", "islamisch"),
        ("SO", "sonstige Religionsgemeinschaft"),
        ("KE", "keiner Religionsgemeinschaft angehörend"),
        ("AL", "alevitisch"),
        ("ME", "mennonitisch"),
        ("FR", "freireligiös"),
    ]
    SEX_CHOICES = [
        ("M", "männlich"),
        ("W", "weiblich"),
        ("D", "divers"),
        ("O", "ohne Eintrag"),
    ]

    COUNTRY_CHOICES = [
        ("DE", "Deutschland"),
        ("UA", "Ukraine"),
        ("SY", "Syrien"),
        ("AF", "Afghanistan"),
        ("AL", "Albanien"),
        ("GI", "Gibraltar (Britisches Überseegebiet)"),
        ("GB", "Guernsey (Britisches Überseegebiet)"),
        ("GB", "Jersey (Britisches Überseegebiet)"),
        ("GB", "Insel Man (Britisches Überseegebiet)"),
        ("NO", "Svalbard und Jan Mayen (u. a. Bäreninsel, Spitzbergen) (Norwegisches Überseegebiet)"),
        ("BA", "Bosnien-Herzegowina"),
        ("AD", "Andorra"),
        ("BE", "Belgien"),
        ("BG", "Bulgarien"),
        ("DK", "Dänemark"),
        ("EE", "Estland"),
        ("FI", "Finnland"),
        ("FR", "Frankreich"),
        ("HR", "Kroatien"),
        ("SI", "Slowenien"),
        ("GR", "Griechenland"),
        ("IE", "Irland"),
        ("IS", "Island"),
        ("IT", "Italien"),
        ("LV", "Lettland"),
        ("ME", "Montenegro"),
        ("LI", "Liechtenstein"),
        ("LT", "Litauen"),
        ("LU", "Luxemburg"),
        ("MK", "Nordmazedonien, ehem. jugosl. Republik"),
        ("MT", "Malta"),
        ("MD", "Moldau, Republik"),
        ("FR", "Monaco"),
        ("NL", "Niederlande"),
        ("NO", "Norwegen"),
        ("XK", "Kosovo"),
        ("AT", "Österreich"),
        ("PL", "Polen"),
        ("PT", "Portugal"),
        ("RO", "Rumänien"),
        ("SK", "Slowakei"),
        ("SM", "San Marino"),
        ("SE", "Schweden"),
        ("CH", "Schweiz"),
        ("RU", "Russland"),
        ("ES", "Spanien"),
        ("TR", "Türkei"),
        ("CZ", "Tschechische Republik"),
        ("HU", "Ungarn"),
        ("VA", "Vatikanstadt"),
        ("GB", "Großbritannien"),
        ("BY", "Belarus"),
        ("XS", "Serbien"),
        ("CY", "Zypern"),
        ("FO", "Färöer (Dänisches Überseegebiet)"),
        ("GB", "Britisches Überseegebiet außerhalb Europas"),
        ("YZ", "Mayotte (Französisches Überseegebiet)"),
        ("FR", "Réunion (Französisches Überseegebiet)"),
        ("ES", "Spanische Hoheitsplätze in Nordafrika (Spanisches Überseegebiet)"),
        ("DZ", "Algerien"),
        ("AO", "Angola"),
        ("ER", "Eritrea"),
        ("ET", "Äthiopien"),
        ("LS", "Lesotho"),
        ("BW", "Botsuana"),
        ("BJ", "Benin"),
        ("DJ", "Dschibuti"),
        ("CI", "Cote d’Ivoire (Elfenbeinküste)"),
        ("NG", "Nigeria"),
        ("ZW", "Simbabwe"),
        ("GA", "Gabun"),
        ("GM", "Gambia"),
        ("GH", "Ghana"),
        ("MR", "Mauretanien"),
        ("CV", "Kap Verde"),
        ("KE", "Kenia"),
        ("KM", "Komoren"),
        ("CG", "Kongo, Republik"),
        ("CD", "Kongo, Dem. Republik"),
        ("LR", "Liberia"),
        ("LY", "Libyen"),
        ("MG", "Madagaskar"),
        ("ML", "Mali"),
        ("MA", "Marokko"),
        ("MU", "Mauritius"),
        ("MZ", "Mosambik"),
        ("NE", "Niger"),
        ("MW", "Malawi"),
        ("ZM", "Sambia"),
        ("BF", "Burkina Faso"),
        ("GW", "Guinea-Bissau"),
        ("GN", "Guinea"),
        ("CM", "Kamerun"),
        ("ZA", "Südafrika"),
        ("RW", "Ruanda"),
        ("NA", "Namibia"),
        ("ST", "São Tomé und Principe"),
        ("SN", "Senegal"),
        ("SC", "Seychellen"),
        ("SL", "Sierra Leone"),
        ("SO", "Somalia"),
        ("GQ", "Äquatorialguinea"),
        ("SD", "Sudan"),
        ("SS", "Südsudan"),
        ("SZ", "Swasiland"),
        ("TZ", "Tansania, Vereinigte Republik"),
        ("TG", "Togo"),
        ("TD", "Tschad"),
        ("TN", "Tunesien"),
        ("UG", "Uganda"),
        ("EG", "Ägypten"),
        ("CF", "Zentralafrikanische Republik"),
        ("BI", "Burundi"),
        ("AW", "Aruba (Niederländisches Überseegebiet)"),
        ("FR", "Französisch-Guayana (Französisches Überseegebiet)"),
        ("VI", "Amerikanische Jungferninseln (US-Überseegebiet)"),
        ("FR", "Guadeloupe (Französisches Überseegebiet)"),
        ("FR", "Martinique (Französisches Überseegebiet)"),
        ("AG", "Antigua und Barbuda"),
        ("CW", "Curaçao (Niederländisches Überseegebiet)"),
        ("BB", "Barbados"),
        ("AR", "Argentinien"),
        ("BS", "Bahamas"),
        ("US", "Puerto Rico (US-Überseegebiet)"),
        ("BO", "Bolivien"),
        ("BR", "Brasilien"),
        ("GY", "Guyana"),
        ("BL", "St. Barthélemy (Französisches Überseegebiet)"),
        ("BZ", "Belize"),
        ("FR", "St. Martin (Französisches Überseegebiet)"),
        ("CL", "Chile"),
        ("DM", "Dominica"),
        ("CR", "Costa Rica"),
        ("DO", "Dominikanische Republik"),
        ("EC", "Ecuador"),
        ("SV", "El Salvador"),
        ("PM", "St. Pierre und Miquelon (Französisches Überseegebiet)"),
        ("GD", "Grenada"),
        ("SX", "St. Martin (niederländischer Teil) (Niederländisches Überseegebiet)"),
        ("GL", "Grönland (Dänisches Überseegebiet)"),
        ("US", "Navassa (US-Überseegebiet)"),
        ("BQ", "Bonaire, Saba, St. Eustatius (Niederländisches Überseegebiet)"),
        ("GT", "Guatemala"),
        ("HT", "Haiti"),
        ("HN", "Honduras"),
        ("CA", "Kanada"),
        ("CO", "Kolumbien"),
        ("CU", "Kuba"),
        ("FR", "Clipperton (Französisches Überseegebiet)"),
        ("MX", "Mexiko"),
        ("NI", "Nicaragua"),
        ("JM", "Jamaika"),
        ("PA", "Panama"),
        ("PY", "Paraguay"),
        ("PE", "Peru"),
        ("SR", "Suriname"),
        ("UY", "Uruguay"),
        ("LC", "St. Lucia"),
        ("VE", "Venezuela"),
        ("US", "USA"),
        ("VC", "St. Vincent und die Grenadinen"),
        ("KN", "St. Kitts und Nevis"),
        ("TT", "Trinidad und Tobago"),
        ("HK", "Hongkong"),
        ("MO", "Macau"),
        ("YE", "Jemen"),
        ("AM", "Armenien"),
        ("BH", "Bahrain"),
        ("AZ", "Aserbaidschan"),
        ("BT", "Bhutan"),
        ("MM", "Myanmar"),
        ("BN", "Brunei Daressalam"),
        ("GE", "Georgien"),
        ("LK", "Sri Lanka"),
        ("VN", "Vietnam"),
        ("KP", "Korea, Demokr. VR"),
        ("IN", "Indien"),
        ("ID", "Indonesien"),
        ("IQ", "Irak"),
        ("IR", "Iran"),
        ("IL", "Israel"),
        ("JP", "Japan"),
        ("KZ", "Kasachstan"),
        ("JO", "Jordanien"),
        ("KH", "Kambodscha"),
        ("QA", "Katar"),
        ("KW", "Kuwait"),
        ("LA", "Laos, Dem. Volksrepublik"),
        ("KG", "Kirgisistan"),
        ("LB", "Libanon"),
        ("MV", "Malediven"),
        ("OM", "Oman, Sultanat"),
        ("MN", "Mongolei"),
        ("NP", "Nepal"),
        ("PS", "Palästinensische Gebiete"),
        ("BD", "Bangladesch"),
        ("PK", "Pakistan"),
        ("PH", "Philippinen"),
        ("TW", "Taiwan"),
        ("KR", "Korea, Republik"),
        ("AE", "Vereinigte Arabische Emirate"),
        ("TJ", "Tadschikistan"),
        ("TM", "Turkmenistan"),
        ("SA", "Saudi-Arabien"),
        ("SG", "Singapur"),
        ("TH", "Thailand"),
        ("ZU", "Usbekistan"),
        ("CN", "China"),
        ("MY", "Malaysia"),
        ("TL", "Timor-Leste"),
        ("ASI", "Übriges Asien"),
        ("HM", "Heard und McDonaldinseln (Australisches Überseegebiet)"),
        ("AU", "Korallenmeerinseln (Australisches Überseegebiet)"),
        ("CC", "Kokosinseln (Australisches Überseegebiet)"),
        ("NC", "Neukaledonien (Französisches Überseegebiet)"),
        ("MP", "Nördliche Marianen (US-Überseegebiet)"),
        ("NF", "Norfolkinseln (Australisches Überseegebiet)"),
        ("AS", "Amerikanisch-Samoa (US-Überseegebiet)"),
        ("TK", "Tokelau (Neuseeländisches Überseegebiet)"),
        ("WF", "Wallis und Futuna (Französisches Überseegebiet)"),
        ("KI", "Weihnachtsinseln (Australisches Überseegebiet)"),
        ("BV", "Bouvetinsel (Norwegisches Überseegebiet)"),
        ("AU", "Australien"),
        ("SB", "Salomonen"),
        ("AU", "Ashmore- und Cartierinseln (Australisches Überseegebiet)"),
        ("FJ", "Fidschi"),
        ("CK", "Cookinseln"),
        ("PF", "Französisch-Polynesien (Französisches Überseegebiet)"),
        ("GU", "Guam (US-Überseegebiet)"),
        ("KI", "Kiribati"),
        ("NR", "Nauru"),
        ("VU", "Vanuatu"),
        ("NU", "Niue"),
        ("UM", "Kleinere Amerikanische Überseeinseln (US-Überseegebiet)"),
        ("NO", "Norwegisches Antarktis-Territorium (Norwegisches Überseegebiet)"),
        ("NZ", "Neuseeland"),
        ("PW", "Palau"),
        ("PG", "Papua-Neuguinea"),
        ("TV", "Tuvalu"),
        ("TO", "Tonga"),
        ("TF", "Französische Süd- und Antarktisgebiete (Französisches Überseegebiet)"),
        ("WS", "Samoa"),
        ("MH", "Marshallinseln"),
        ("FM", "Mikronesien"),
        ("CL", "Chilenische Antarktis (Chilenisches Überseegebiet)"),
        ("AU", "Australisches Antarktis-Territorium (Australisches Überseegebiet)"),
        ("AR", "Argentinische Antarktis (Argentinisches Überseegebiet)"),
        ("NZ", "Neuseeländische Antarktis: Ross-Nebenbiet (Neuseeländisches Überseegebiet)"),
        ("NN", "Staatenlos"),
        ("NN", "Ungeklärt"),
        ("NN", "ohne Angabe Staatsangehörigkeit"),
    ]

    LANGUAGE_CHOICES = [
        ("", "Deutsch"),
        ("UKR", "Ukrainisch"),
        ("ARA", "Arabisch"),
        ("FA", "Farsi (Persisch)"),
        ("DAR", "Dari (Persisch)"),
        ("ENG", "Englisch"),
        ("FRA", "Französisch"),
        ("ALB", "Albanisch"),
        ("BOS", "Bosnisch"),
        ("ZH", "Chinesisch"),
        ("ITA", "Italienisch"),
        ("KRO", "Kroatisch"),
        ("POL", "Polnisch"),
        ("POR", "Portugiesisch"),
        ("RUS", "Russisch"),
        ("SMO", "Serbisch"),
        ("SLO", "Slowenisch"),
        ("SPA", "Spanisch"),
        ("TÜR", "Türkisch"),
        ("GRI", "Griechisch"),
        ("ASI", "Sonstige asiatische Sprache"),
        ("AFR", "Afrikanische Sprache"),
        ("KUR", "Kurdisch (Sorani)"),
        ("UNK", "Sonstige Sprache"),
        ("BGR", "Bulgarisch"),
        ("ROU", "Rumänisch"),
        ("CZE", "Tschechisch"),
        ("HUN", "Ungarisch"),
        ("VI", "Vietnamesisch"),
    ]

    EXAM_CHOICES = [
        ("OB", "Abgangszeugnis ohne Berufsreife"),
        ("AO", "Abgangszeugnis im FSP G ohne Berufsreife"),
        ("FÖ", "Abschlusszeugnis FSP L, ohne Berufsreife"),
        ("BR", "Berufsreife (Hauptschulabschluss)"),
        ("S1", "Qualifizierter Sekundarabschluss I (Mittlere Reife)"),
        ("FGH", "Fachgebundene Hochschulreife"),
        ("AH", "Allgemeine Hochschulreife"),
        ("NV", "nicht vergleichbarer Abschluss ausländisch. Schule"),
        ("FHST", "Fachhochschulreife (schulischer Teil)"),
        ("FHSPT", "Fachhochschulreife (schulischer und prakt. Teil)"),
    ]

    GUARDIAN_CHOICES = [
        ("Mu", "Mutter"),
        ("Va", "Vater"),
        ("PfMu", "Pflegeutter"),
        ("PfVa", "Pflegevater"),
        ("Vo", "Vormund"),
    ]

    LASTSCHOOL_CHOICES = [
        ("HS", "Hauptschule"),
        ("FWS", "Freie Waldorfschule"),
        ("KOLLAGY", "Kolleg / Abendgymnasium"),
        ("RS", "Realschule"),
        ("RS+", "Realschule plus"),
        ("GY", "Gymnasium"),
        ("FOES", "Förderschule"),
        ("IGS", "Integrierte Gesamtschule"),
        ("BBS", "Berufsbildende Schule"),
        ("FOS", "Fachoberschule"),
        ("SONST", "Sonstiger Zugang"),
    ]

    LASTCLASS_CHOICES = [
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
        ("13", 13),
    ]
    id = HiddenField("ID", validators=[Optional()])
    schulform = HiddenField("Schulform", validators=[Optional()])

    # Stammdaten
    klassenbezeichnung = SelectField(
        "Klasse",
        choices=[("", "Bitte wählen...")],
        validators=[DataRequired(message="Bitte deine Klasse auswählen.")],
        render_kw={"title": "Bitte wähle deine neue Klasse aus."},
    )
    schueler_religion = SelectField(
        "Religion",
        choices=[("", "Bitte wählen...")] + RELIGION_CHOICES,
        validators=[DataRequired(message="Bitte deine Religion auswählen.")],
        render_kw={"title": "Bitte deine Religion auswählen."},
    )
    eintrittsdatum = DateField(
        "Eintrittsdatum",
        format="%Y-%m-%d",
        default=bbs_eintrittsdatum,
        validators=[DataRequired()],
        render_kw={"title": "Das Datum, an dem du zum ersten Mal an der BBS sein solltest"},
    )

    schueler_familienname = StringField(
        "Nachname",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: Müller"},
    )
    schueler_vorname = StringField(
        "Vorname",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: Thomas"},
    )
    schueler_geburtsdatum = DateField(
        "Geburtsdatum",
        format="%Y-%m-%d",
        default=schueler_geburtsdatum,
        validators=[DataRequired(message="Bitte trage dein Geburtsdatum ein.")],
        render_kw={"title": "Bitte trage dein Geburtsdatum ein."},
    )
    schueler_geburtsort = StringField(
        "Geburtsort",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: Trier"},
    )
    schueler_geschlecht = SelectField(
        "Geschlecht",
        choices=[("", "Bitte wählen...")] + SEX_CHOICES,
        validators=[DataRequired(message="Bitte wähle dein Geschlecht aus")],
        render_kw={"title": "Bitte wähle dein Geschlecht aus"},
    )
    schueler_staatsangehörigkeit = SelectField(
        "Staatsangehörigkeit",
        choices=[("", "Bitte wählen...")] + COUNTRY_CHOICES,
        validators=[DataRequired(message="Bitte eine Staatsangehörigkeit auswählen.")],
        render_kw={"title": "Bitte wähle deine Staatsangehörigkeit aus."},
    )
    schueler_familiensprache = SelectField(
        "Familiensprache",
        choices=[("", "Bitte wählen...")] + LANGUAGE_CHOICES,
        validators=[Optional()],
        render_kw={"title": "Bitte wähle die Sprache aus, in der du mit deinen Eltern sprichst."},
    )
    schueler_geburtsland = SelectField(
        "Geburtsland",
        choices=[("", "Bitte wählen...")] + COUNTRY_CHOICES,
        validators=[DataRequired(message="Bitte dein Geburtsland auswählen.")],
        render_kw={"title": "Bitte wähle dein Geburtsland aus."},
    )
    schueler_strasse = StringField(
        "Straße",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: Rittersdorferstrasse"},
    )
    schueler_hausnummer = StringField(
        "Hausnummer",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: 2a"},
    )
    schueler_PLZ = StringField(
        "PLZ",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: 54634"},
    )
    schueler_wohnort = StringField(
        "Wohnort",
        validators=[DataRequired()],
        render_kw={"placeholder": "z.B.: Bitburg"},
    )
    schueler_stadtteil = StringField(
        "Stadtteil (wenn vorhanden)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Pallien"},
    )

    schueler_telefon_1 = StringField(
        "Telefon (Mobil)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: +49 (175) 987 654 3"},
    )
    schueler_telefon_2 = StringField(
        "Telefon (Festnetz)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: +49 (651) 987 654 3"},
    )
    schueler_email = EmailField(
        "E-Mail",
        validators=[Optional(), Email(message="Bitte gieb eine gültige E-Mail-Adresse ein.")],
        render_kw={"placeholder": "z.B.: sekreatariat@tssbit.de"},
    )

    # erziehungsberechtigte_2
    erziehungsberechtigte_1_name = StringField(
        "Name",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Müller"},
    )
    erziehungsberechtigte_1_vorname = StringField(
        "Vorname",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Maria"},
    )
    erziehungsberechtigte_1_PLZ = StringField(
        "PLZ",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: 54634"},
    )
    erziehungsberechtigte_1_wohnort = StringField(
        "Wohnort",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Bitburg"},
    )
    erziehungsberechtigte_1_stadtteil = StringField(
        "Stadtteil",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Erdorf"},
    )
    erziehungsberechtigte_1_strasse = StringField(
        "Straße",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Ritterdorferstrasse 2"},
    )
    erziehungsberechtigte_1_hausnummer = StringField(
        "Hausnummer",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: 2a"},
    )

    erziehungsberechtigte_1_telefon_1 = StringField(
        "Telefon (Mobil)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: +49 (175) 987 654 3"},
    )
    erziehungsberechtigte_1_telefon_2 = StringField(
        "Telefon (Festnetz)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: +49 (651) 987 654 3"},
    )
    erziehungsberechtigte_1_email = EmailField(
        "E-Mail",
        validators=[Optional(), Email()],
        render_kw={"placeholder": "z.B.: sekreatariat@tssbit.de"},
    )
    erziehungsberechtigte_1_art = SelectField(
        "Art der/des Erziehungsberechtigten",
        choices=[("", "Bitte wählen...")] + GUARDIAN_CHOICES,
        validators=[Optional()],
        render_kw={"title": "Bitte wähle den Erziehungsberechtigten aus."},
    )

    # erziehungsberechtigte_2
    erziehungsberechtigte_2_name = StringField(
        "Name",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Müller"},
    )
    erziehungsberechtigte_2_vorname = StringField(
        "Vorname",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Maria"},
    )
    erziehungsberechtigte_2_PLZ = StringField(
        "PLZ",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: 54634"},
    )
    erziehungsberechtigte_2_wohnort = StringField(
        "Wohnort",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Bitburg"},
    )
    erziehungsberechtigte_2_stadtteil = StringField(
        "Stadtteil",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Erdorf"},
    )
    erziehungsberechtigte_2_strasse = StringField(
        "Straße",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: Ritterdorferstrasse 2"},
    )
    erziehungsberechtigte_2_hausnummer = StringField(
        "Hausnummer",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: 2a"},
    )

    erziehungsberechtigte_2_telefon_1 = StringField(
        "Telefon (Mobil)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.: +49 (175) 987 654 3"},
    )
    erziehungsberechtigte_2_telefon_2 = StringField(
        "Telefon (Festnetz)",
        validators=[Optional()],
        render_kw={"placeholder": "z.B.:+49 (651) 987 654 3"},
    )
    erziehungsberechtigte_2_email = EmailField(
        "E-Mail",
        validators=[Optional(), Email()],
        render_kw={"placeholder": "z.B.: sekreatariat@tssbit.de"},
    )
    erziehungsberechtigte_2_art = SelectField(
        "Art der/des Erziehungsberechtigten",
        choices=[("", "Bitte wählen...")] + GUARDIAN_CHOICES,
        validators=[Optional()],
        render_kw={"title": "Bitte wähle den Erziehungsberechtigten aus."},
    )

    # Schulhistorie
    grundschule_datum = DateField(
        "Einschulung in Grundschule ",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        default=schueler_grundschuldatum,
        render_kw={
            "placeholder": "z.B.:  01.08.2005",
            "title": "Wenn du nur das Jahr kennst, nehme den 01.08. als Tag und Monat",
        },
    )
    letzte_schule_name = StringField(
        "Name der letzten Schule",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "z.B.:  Otto-Hahn-Realschule Plus",
            "title": "Der Name deiner letzten Schule",
        },
    )
    letzte_schule_ort = StringField(
        "Ort der letzten Schule",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "z.B.: Bitburg",
            "title": "In welcher Stadt war diese Schule?",
        },
    )

    letzte_schule_schulart = SelectField(
        "Schulart",
        choices=[("", "Bitte wählen...")] + LASTSCHOOL_CHOICES,
        validators=[DataRequired(message="Bitte wähle deine letzte Schule aus")],
        render_kw={"title": "Was für eine Schule war das?(Realschule, Gesamtschule, ...)"},
    )
    letzte_schule_klasse = SelectField(
        "Jahrgangsstufe der letzten Klasse",
        choices=[("", "Bitte wählen...")] + LASTCLASS_CHOICES,
        validators=[DataRequired(message="Bitte gib eine Zahl zwischen 9 und 13 ein.")],
        render_kw={"placeholder": "z.B.: 10", "title": "9–13"},
    )
    letzte_schule_abschluss = SelectField(
        "Erreichter Abschluss",
        choices=[("", "Bitte wählen...")] + EXAM_CHOICES,
        validators=[DataRequired(message="Bitte wähle deinen letzten Schulabschluss aus.")],
        render_kw={
            "title": "Bitte wähle deinen letzten Schulabschluss aus.",
        },
    )
    letzte_schule_abgangsdatum = DateField(
        "Abgangsdatum",
        format="%Y-%m-%d",
        default=bbs_eintrittsdatum,
        validators=[DataRequired(message="Das Datum, an dem du zum ersten Mal an der BBS sein solltest")],
        render_kw={"title": "Das Datum, an dem du zum ersten Mal an der BBS sein solltest"},
    )
    abschluss_maximal = SelectField(
        "Maximaler Abschluss",
        choices=[("", "Bitte wählen...")] + EXAM_CHOICES,
        validators=[DataRequired(message="Bitte wähle deinen höchsten Schulabschluss aus.")],
        render_kw={"title": "Bitte wähle deinen höchsten Schulabschluss aus."},
    )

    # Zusatzangaben

    auslaender_foerderbedarf_deutsch = BooleanField(
        "Förderbedarf Deutsch",
        default=False,
        render_kw={
            "title": "Benötigst du einen zusätzlichen Deutschkurs?",
        },
    )
    auslaender_einreisedatum = DateField(
        "Einreisedatum",
        format="%Y-%m-%d",
        validators=[Optional()],
        render_kw={"title": "Wenn du nur das Jahr kennst, nehme den 01.08. als Tag und Monat"},
    )


class VollzeitschuelerForm(SchuelerBaseForm):
    """WTF_Form zur Benutzung in folgenden Routen:
    @app.route("/")
    @app.route("/vollzeitschule.html"
    """

    submit = SubmitField("Vollzeitschüler speichern")

    def __repr__(self):
        return "<VollzeitschuelerForm:>"


class BerufsschuelerForm(SchuelerBaseForm):
    """WTF_Form zur Benutzung in folgenden Routen:
    @app.route("/berufsschule.html
    """

    PROFFESSION_CHOICES = [
        ("AK", "Automobilkaufleute"),
        ("SHK", "Anlagenmechaniker (SHK)"),
        ("BA", "Bankkaufleute"),
        ("BM", "Kaufleute für Büromanagement"),
        ("EK", "Kaufleute im Einzelhandel"),
        ("EEG", "Elektroinstallateure"),
        ("FR", "Friseurinnen"),
        ("IM", "Industriemechaniker"),
        ("IMO", "Immobilienkaufleute"),
        ("ITSysEL", "IT-Systemelektroniker"),
        ("DM", "Kaufleute für Digitalisierungsmanagement"),
        ("KonK", "Konstruktionsmechaniker"),
        ("Karr", "Karosseriebauer"),
        ("SM", "Kaufleute für IT-Systemmangement"),
        ("KM", "KFZ-Mechatroniker"),
        ("LBM", "Land-und Baumaschinenmechaniker"),
        ("ML", "Maler/Lackierer"),
        ("MT", "Metalltechnik"),
        ("SF", "Steuerfachangestellte"),
        ("TI", "Tischler"),
        ("VK", "Verkäufer"),
        ("WM", "Werkzeugmechaniker"),
        ("ZIM-FT", "Zweiradmechechatroniker (Fahrradtechnik)"),
        ("ZIM-MT", "Zweiradmechechatroniker (Motorradtechnik)"),
        ("ZSP", "Zerspanungsmechaniker"),
    ]

    # Betriebliche Attribute
    betrieb_name = StringField(
        "Betrieb Name",
        validators=[DataRequired(message="Bitte den Betriebsnamen angeben.")],
        render_kw={"placeholder": "z.B.: Hutfabrik Duck GmbH"},
    )
    betrieb_anprechpartner_name = StringField(
        "Ansprechpartner Name",
        validators=[DataRequired(message="Bitte den Nachnamen des Ausbilders angeben.")],
        render_kw={
            "placeholder": "z.B.: Duck",
            "title": "Wie lautet der Nachname deines Ausbilders",
        },
    )
    betrieb_anprechpartner_vorname = StringField(
        "Ansprechpartner Vorname",
        validators=[DataRequired(message="Bitte den Vornamen des Ausbilders angeben.")],
        render_kw={
            "placeholder": "z.B.: Dagobert",
            "title": "Wie lautet der Vorname deines Ausbilders",
        },
    )
    betrieb_PLZ = StringField(
        "Betrieb PLZ",
        validators=[DataRequired(message="Bitte die PLZ des Betriebs angeben.")],
        render_kw={"placeholder": "z.B.: 12345"},
    )
    betrieb_ort = StringField(
        "Betrieb Ort",
        validators=[DataRequired(message="Bitte den Ort des Betriebs angeben.")],
        render_kw={
            "placeholder": "z.B.: Entenhausen",
            "title": "Wie lautet der Ort deines Ausbildungsbetriebes",
        },
    )
    betrieb_strasse = StringField(
        "Betrieb Straße",
        validators=[DataRequired(message="Bitte die Adresse des Betriebs angeben.")],
        render_kw={
            "placeholder": "z.B.: Zum Geldspeicher 5",
            "title": "Wie lautet die Adresse deines Ausbildungsbetriebes",
        },
    )
    betrieb_telefon = StringField(
        "Betrieb Telefon",
        validators=[Optional()],
        render_kw={
            "placeholder": "z.B.: +49 (175) 987 654 3",
            "title": "Unter welcher Telefonnummer kann man deinen Betrieb erreichen?",
        },
    )
    betrieb_email = EmailField(
        "Ansprechpartner E-Mail",
        validators=[DataRequired(message="Bitte die E-Mail des Ausbilders angeben."), Email()],
        render_kw={
            "placeholder": "z.B.: dagobert@duck.com",
            "title": "Wie lautet die Mailadresse deines Ausbilders",
        },
    )

    ausbildung_beruf = SelectField(
        "Ausbildungsberuf",
        choices=[("", "Bitte wählen...")] + PROFFESSION_CHOICES,
        validators=[DataRequired(message="Bitte den Ausbildungsberuf angeben.")],
        render_kw={
            "title": "In welchem Ausbildungsberuf wirst du ausgebildet? ",
        },
    )

    ausbildung_start = DateField(
        "Ausbildungsstart",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Bitte das Startdatum der Ausbildung angeben.")],
        render_kw={
            "title": "An welchem Tag begann deine Ausbildung im Betrieb?",
        },
    )
    ausbildung_ende = DateField(
        "Ausbildungsende",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Bitte das Enddatum der Ausbildung angeben.")],
        render_kw={
            "title": "Wann wird deine Ausbildung im Betrieb enden? (Wähle den 1. August in 3 Jahren, wenn du ihn nicht kennst)",
        },
    )
    ausbildung_kammer = SelectField(
        "Kammer",
        choices=[("", "Bitte wählen...")] + [("IHK", "IHK"), ("HWK", "HWK")],
        validators=[DataRequired(message="Bitte eine Kammer auswählen.")],
        render_kw={
            "title": "Wähle die Kammer der dein Betrieb angeschlossen ist.",
        },
    )

    submit = SubmitField("Berufsschüler speichern")

    def __repr__(self):
        return "<BerufsschuelerForm:>"


class SchuelerAuswahlForm(FlaskForm):
    """WTF_Form zur Benutzung in folgenden Routen:
    @app.route("/route_schueleranzeige.html"
    """

    klassen = SelectField(
        "Welche Klasse soll angezeigt werden / wollen Sie herunterladen?",
        validators=[DataRequired(message="Bitte wählen Sie eine Klasse aus.")],
    )
    schulform = HiddenField(
        "schulform",
        validators=[DataRequired()],
        render_kw={"id": "form_schulform"},
    )
    submit_csv = SubmitField("Download-CSV", render_kw={"class": "btn btn-primary midi"})
    submit_pdf = SubmitField("Download-PDF", render_kw={"class": "btn btn-primary midi"})
    submit_xlsx = SubmitField("Download-XLSX", render_kw={"class": "btn btn-primary midi"})


class FileuploadForm(FlaskForm):
    """WTF_Form zur Benutzung in folgenden Routen:
    @app.route("/upload.html
    """

    upload_file = FileField(
        "Datei auswählen",
        validators=[
            FileAllowed(["csv", "pdf"], "Nur CSV- und PDF-Dateien sind erlaubt!"),
        ],
    )
    submit = SubmitField(
        "Download",
        render_kw={"class": "btn btn-primary small"},
    )
