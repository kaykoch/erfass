# erfass

Digitaler Erfassungsbogen für Vollzeit- und Berufsschüler zum späteren Import in edoosys.  Es handelt sich um eine  Webapplikation in Python mit Datenbank und Webserver.
Die App kann auf jedem schulinternen Server installiert werden, oder auch auf einem Server außerhalb.

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
- Programm starten: (Sollte die die App nicht starten, liegt es vieleicht daran, dass sie nicht ausführbar ist)
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

Der Aufruf erfolgt mit: 
   ```
  http://localhost:5000/
  ``` 

bzw. für die Administration:  (Benutzername: admin | Password: admin)
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

## Benutzung
> Wird fortgesetzt