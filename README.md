# Hardwaresteuerung
Mitwirkende:
- Michael Hopp
- Niclas Jarowsky
- Ammar Morshed
- Adrian Petzold

## Hardware Aufbau
- Roboterarm mit 4 Servomotoren (Servos werden gemäß ihrer Position/Wirkung bezeichnet: **Schulter**/Oberarm, **Ellenbogen**/Unterarm, **Handgelenk**/Hand und Finger/**Stift**)
- Liegendes Spielfeld A4-Blatt mit 7x6 Raster unter Plexiglasscheibe
- Steckbrett
- Raspberry Pi (3B) & Netzkabel
- Labornetzteil
- Knopf (Zugende)
- Stift

**Aufbauskizze:**

![Aufbauskizze](https://github.com/WS22-Robotik-4-Gewinnt/Hardwaresteuerung/blob/main/assets/images/Aufbauskizze.png?raw=true)

**Aufbau Photo:**

![Aufbau abfotografiert](https://github.com/WS22-Robotik-4-Gewinnt/Hardwaresteuerung/blob/main/assets/images/Robotik%20Roboarm%20Aufbau.jpeg?raw=true)


TODO: Schaltplan hinzufügen

## Logindaten PI:
```
username: pi
password: asdf1234
```

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
###  Bildverarbeitung -> Spielalgorithmus
```json
{ "Column1": {"Row1":"h", "Row2":"0", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column2": {"Row1":"0", "Row2":"0", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column3": {"Row1":"0", "Row2":"0", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column4": {"Row1":"0", "Row2":"0", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column5": {"Row1":"0", "Row2":"0", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column6": {"Row1":"h", "Row2":"h", "Row3":"h", "Row4":"0", "Row5":"0", "Row6":"0"},
"Column7": {"Row1":"r", "Row2":"r", "Row3":"0", "Row4":"0", "Row5":"0", "Row6":"0"}
}
```

### Übertragung Spielalgorithmus -> Hardwaresteuerung
```json
{
 "col": 7,
 "row": 1
}
```
### Fast API starten
```commandline
uvicorn main:app --reload --host 0.0.0.0 --port 8096
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
16. 
17. TODO
18. 
19. Change Request: Spielergebnis soll mit LEDs dargestellt werden.
20. Change Request: Schwierigkeitsgrad des Computergegners soll per Knopfdruck änderbar sein + Anzeige per LEDs.
