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
- Erstellen eines Zielordners: ``` mkdir erfass ```
- Herunterladen der App ```git clone https://github.com/kaykoch/erfass.git```
- In Ordner hineinspringer ``` cd erfass ```
- Setup-Programm starten: ```python3 setup.py```

## Programmstart

### Lokal

Wenn das Programm zum testen auf dem lokalen PC gestartet werden soll:
- venv starten (im Ordner "erfass"): ```source .venv/bin/activate```
- Programm starten: ```./erfass.py``` (Sollte die die App nicht starten, liegt es vieleicht daran, dass erfass.py nicht ausführbar ist)\
In dem Fall:

- entweder jedes Mal: ```python3 ./erfass.py```
- oder (dringend empfohlen) einmalig die Datei ausführbar machen: ``` chmod +x erfass.py ```

    und in Zukunft, wie beschrieben: ``` ./erfass.py```

Der Aufruf erfolgt mit: 

 ```http://localhost:5000```

bzw. mit:

  ```http://localhost:5000/admin``` (Benutzername: admin | Password: admin)

### Server

Wenn das Programm im produktiven Einsatz laufen, kommt GuniCorn ins Spiel. \
Hierfür gibt es das Startscript: ```startGunicorn.py```
(Es gilt für die Ausführbarkeit das gleiche wie oben.) 

**startGunicorn.py:** \
Es gibt drei Parameter im script, die man ändern kann: (In Klammer die Default-Werte)

1. APP_NAME: beliebiger Name, Dient nur zur Unterscheidung bei mehreren GuniCorn Anwendungen (erfass)
2. PORT : Port auf dem der Server hören soll (8081)
3. WORKERS: Anzahl der Instanzen, die von Gunicorn gestartet werden sollen. Nur interessant bei zu erwartender hoher Last (1)