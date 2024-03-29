# Hardwaresteuerung
Mitwirkende:
- Michael Hopp
- Niclas Jarowsky
- Ammar Morshed
- Adrian Petzold
- Frieder Ullmann (Docker)

## Hardware Aufbau
- Roboterarm mit 4 Servomotoren (Servos werden gemäß ihrer Position/Wirkung bezeichnet: **Schulter**/Oberarm, **Ellenbogen**/Unterarm, **Handgelenk**/Hand und Finger/**Stift**)
- Liegendes Spielfeld A4-Blatt mit 7x6 Raster unter Plexiglasscheibe
- Steckbrett
- Raspberry Pi (3B) & Netzkabel
- Labornetzteil
- Knopf (Zugende)
- Stift

**Aufbauskizze:**

![Aufbauskizze](/assets/images/Aufbau%20Skizze.png)

**Aufbau Photo (ohne Kamera):**

![Aufbau abfotografiert](/assets/images/Robotik%20Roboarm%20Aufbau.jpeg)


**Schaltplan:**
![Schaltplan Bild](/assets/images/Schaltplan_Robotik_Pi4_Steckplatine.png)

## Datenstruktur
Das Spielfeld der Hardwaresteuerung wird als ein zweidimensionales Array dargestellt, welches bei 0 beginnt! Demnach muss von dem Input der Spiellogik -1 genommen werden (col 1 in Spielalgorithmus ist 0 in Hardwaresteuerung).

### Spielfeld 7x6
```
6 0  0  0  0  0  0  0
5 0  0  0  0  0  0  0
4 0  0  0  0  0  0  0
3 h  0  0  r  0  0  0
2 h  r  r  h  r  0  r
1 h  h  h  r  h  r  r
--1--2--3--4--5--6--7

// h = Human Player | r = Robot Player | 0 = empty space
```

## Schnittstellen / Kommunikation

### Übertragung Spielalgorithmus -> Hardwaresteuerung
**Zug**
```json
{
 "col": 7,
 "row": 1
}
```
**Spielergebnis**
```json
{
 "winner": "human"
}
```

### Fast API starten
```commandline
uvicorn src.main:app --reload --host 0.0.0.0 --port 8096
```

### Docker bauen und starten
```commandline
docker build -t hardware .
docker run --device /dev/gpiomem -d -p 8096:8096 hardware
docker run --privileged -d -p 8096:8096 hardware
```

## Projektverlauf
1. Hardware empfangen: Roboterarm mit Spielfeld und Steckbrett + Kabeln.
2. Geräte umziehen in einen anderen Raum der FH und Schlüsselbeschaffung.
3. Funktionsfähigkeit der Servomotoren des Roboterarms mit einem Arduino prüfen: Je Servomotor, alle möglichen Positionen durchlaufen lassen und Winkel für den Spielbereich festhalten (Schulter braucht nur maximal 90° abzudecken: Bewegt sich von -90° bis 0°).
4. Privaten Raspberry Pi 3B anschließen (Christian Harders): Es gilt zu beachten, den korrekten Pin-Schaltplan zu verwenden. Außerdem muss ein passendes Netzteil angeschlossen werden. Bei der Verwendung von RPi und Arduino, trat folgendes Phänomen auf: Obwohl der Arduino nicht an den Roboterarm angeschlossen war, reagierten die Servos auf seine Signale, solange der Arduino in einer benachbarten Steckdose angeschlossen wurde.
5. Permanent-Marker gegen einen wasserlöslichen austauschen.
6. In Python die notwendigen Funktionen zum operieren des Roboterarms entwickeln
7. Winkelkonfigurationen der Servos ermitteln, um das erste Feld (0,0) anzufahren und als Ausgangsbasis für alle anderen Felder nutzen. Zweidimensionales Array für die Winkeleinstellungen des gesamten Spielfeldes entwickeln. Zugriff auf die jeweiligen Felder erfolgt ab nun über diese Matrix.
8. Festlegen der Parkposition des Roboterarms.
9. Test-Programm schreiben, welches jedes Feld anfährt und markiert.
10. Feinjustierung der Stärke des Aufdrückens des Stifts und Servo-Winkelkonfigurationen einzelner Felder.
11. Change Request umsetzen: Es soll ein Button eingebaut werden, der dem Computer vermittelt, dass der menschliche Spieler seinen Zug beendet hat, sodass es sicherer ist, den Roboterarm nach dieser "Freigabe" schwenken zu lassen. Dieser Knopfdruck wird dazu verwendet, die Spiellogik und die Bildverarbeitung anzustoßen, sodass das Spielfeld zum Zeitpunkt des Knopfdruckes ausgewertet und ein Gegenzug ermittelt wird, der dann umgehend an die Hardwaresteuerung vermittelt wird.
12. Besprechung der Schnittstellenspezifikationen zur Kommunikation zwischen den Modulen/APIs.
13. Programmierung eines Python Skriptes, das Tastatureingaben x (col) und y (row) abfragt, um bereits interaktiv (ohne Computergegner) spielen zu können.
14. Umsetzung der Steuerung des Roboterarms als REST-Api (FastApi mit ARC als UI) gemäß Vorgaben der Schnittstellenspezifikation.
15. Zur Verhinderung, dass die Servomotoren gegenseitig "Jitter" erzeugen, wurde die Library Py GPIO Factory eingebaut. Dadurch passen die Winkelkonfigurationen der Servos nicht mehr! Erneute Kalibrierung jedes einzelnen Feldes (Anpassung der Matrix).
16. Change Request: Spielergebnis soll mit LEDs dargestellt werden. Installation einer LED-Matrix
17. Integrationstest mit den Modulen Spiellogik und Kamera
18. Für vereinfachte Bilderkennung einrichten, dass statt Punkten, Striche gezeichnet werden
19. Anschluss der LED Matrix für Anzeige des Schwierigkeitsgrades und des Siegers zum Spielende
20. Anschluss eines weiteren Knopfes für das Iterieren durch die Schwierigkeitsgrade
21. "Wiggle" (Striche statt Punkten zeichnen) optimiert
22. Dockerfile erstellt
23. Neuinstallation des Systems auf "sauberem" Raspberry Pi
