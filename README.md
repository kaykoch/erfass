# erfass

Digitaler Erfassungsbogen für Vollzeit- und Berufsschüler zum späteren Import in edoosys.  Es handelt sich um eine  Webapplikation in Python mit Datenbank und Webserver.
Die App kann auf jedem schulinternen Server installiert werden, oder auch auf einem Server außerhalb.
Ursprünglich war die App nur als Alternative zum Erfassungsbogen unserer Schule gedacht, den die Schüler nach beginn des Schuljahres ausfüllen. Zu diesem Zeitpunkt war die Klasse bereits bekannt. Daher die Möglichkeit der Auswahl der Klasse.
Jetzt ist das primäre Ziel der Import in edoosys als Bewerber.

## Installation
Die Installation erfolgt über setup.py. Das Programm installiert eine virtuelle Umgebung und alle notwendigen Bibliotheken.
Zusätzlich wird [Gunicornn](https://gunicorn.org) instaliert. Ein Web Server Gateway Interface (WSGI) HTTP Server 

### Voraussetzungen
Auf dem Server muss python3 (>= 3.11), pip3 und python3-venv installiert sein
Je nach dem, wie Ihr das repository herunterladet muss noch git oder zip installiert werden

### Installation
```bash 
mkdir erfass                                    # Erstellen eines Zielordners
cd erfass                                       # In Ordner hineinspringer
git clone https://github.com/kaykoch/erfass.git # Herunterladen der App
python3 setup.py                                # Setup-Programm starten
```
## Programmstart
### Lokal
Wenn das Programm zum testen auf dem lokalen PC gestartet werden soll:
- venv starten (im Ordner "erfass"): 
```bash 
source .venv/bin/activate
```
- Programm starten: (Sollte die die App nicht starten, liegt es vielleicht daran, dass sie nicht ausführbar ist)
```bash 
./erfass.py
```
In dem Fall:

- entweder jedes Mal: 
```bash
python3 ./erfass.py
```
- oder (dringend empfohlen) einmalig die Datei ausführbar machen: 
```bash
 chmod +x erfass.py 
 ```
und in Zukunft, wie beschrieben: 
```bash 
./erfass.py
```

**erfass.py:** \
Man kann die App im Debug Mode laufen lassen. Das führt dazu, dass bei Änderungen am Code nicht neu gestartet werden muss. \
Im Quelltext:

```python
app.run(debug=False) # (! ZWINGEND FÜR SERVEREINSATZ !) 
```

```python
app.run(debug=True) # App startet selbstständig neu (! NUR FÜR DEN LOKALEN EINSATZ !) 
``` 

Der Aufruf erfolgt im Browser mit: 
   ```
  http://localhost:5000/
  ``` 

bzw. für die Administration:  (Login: admin | Password: admin)
  ```
  http://localhost:5000/admin
  ``` 
 

### Server
Wenn das Programm im produktiven Einsatz laufen, kommt GuniCorn ins Spiel. \
Hierfür gibt es das Startscript: (Es gilt für die Ausführbarkeit das gleiche wie oben.) 
```bash 
startGunicorn.py
```


**startGunicorn.py:** \
Es gibt drei Parameter im script, die man ändern kann:\
Im Quelltext:
```python
APP_NAME = "erfass"  # beliebiger Name für die Applikation. Dient nur zur Unterscheidung bei mehreren GuniCorn Anwendungen
PORT = "8081"  # Port auf dem der Server hört
WORKERS = 1  # Anzahl der gestarteten Dienste .Nur interessant bei zu erwartender hoher Last
```
Der Aufruf erfolgt im Browser mit: 
   ```
  http://<SERVER_URL>:PORT/
  ``` 

bzw. für die Administration:
  ```
http://<SERVER_URL>:PORT//admin
  ``` 
 
## Benutzung
### Schüler
![alt text](static/benutzer.jpg)
- Auswahl von Vollzeit- oder Berufsschüler
  - -> Unterschiedliche Klassen und Bereiche
- Auswahl von Klassen
  - -> unterschiedliche Klassen, je Schulform + UNBEKANNT für Bewerber \
      (Kann per Datei jedes Jahr neu hochgeladen werden)
- Vorbesetzung von Daten (Plural von Datum)
  - -> Eintrittsdatum: dieses 01.08.aktuelles_Jahr
  - -> Geburtsdatum: 01.01.Vor_17_Jahren
  - -> Einschulung: 01.08.Geburtjahr + 6 
- Auswahl Minderjährig
 - -> Ein- oder ausblenden von 2 Erziehungsberechtigten
 - Betriebliche Angaben bei Berufsschülern
  -> Auswahl von Berufen
    (Fest codiert)

### Administration
- Auswahl von Vollzeit- oder Berufsschüler
  - -> Auswahl zur Anzeige bestimmter Klassen oder aller Schüler
  - -> nach Auswahl:
    - -> Auswahl einzelner Schüler zur Änderung von Schülerdaten in selber Maske wie Schülereingabe
    - -> Download der angezeigten Schüler als PDF (ein Blatt pro Schüler)
    - -> Download der angezeigten Schüler als CSV zur weiteren Verarbeitung für Notenhefte, Server-Accounts, Mailprogramme, usw.
    - -> Download der angezeigten Schüler als XLSX zum Import in edoosys    
- Konfigurationsseite   
  - -> Administrationslogin und -passwort
  - -> Zugangsdaten für Mailaccount (Vielleicht für später)
- Upload Klassenliste
  - -> Upload einer CSV-Datei mit den Klassennamen des aktuellen Schuljahres und der Unterscheidung zwischen Vollzeit- und Berufsschule.
  - -> Download einer Musterdatei
> Wird fortgesetzt
