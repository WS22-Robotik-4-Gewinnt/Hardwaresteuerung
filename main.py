import json
from gpiozero import AngularServo, Button, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from fastapi import FastAPI, Request
import requests

app = FastAPI()
Device.pin_factory = PiGPIOFactory()

lookupTable = [[[-20, 55, 2], [-37, 80, -2], [-50, 85, 23], [-59, 86, 43], [-64, 87, 60], [-68, 87, 75]],
               [[-32, 58, 10], [-48, 80, 12], [-61, 85, 32], [-69, 86, 50], [-77, 87, 66], [-83, 88, 80]],
               [[-40, 62, 10], [-57, 80, 17], [-70, 85, 36], [-80, 86, 54], [-83, 78, 78], [-90, 80, 90]],
               [[42, -26, -40], [53, -36, -52], [64, -48, -60], [77, -60, -65], [90, -72, -72], [90, -65, -90]],
               [[48, -65, -5], [64, -80, -14], [75, -86, -30], [82, -86, -44], [85, -80, -64], [86, -76, -81]],
               [[41, -65, 0], [55, -80, -10], [66, -85, -26], [73, -86, -41], [77, -85, -57], [83, -89, -68]],
               [[30, -58, 0], [47, -80, -4], [56, -85, -20], [63, -86, -37], [66, -84, -53], [68, -85, -65]]]

stift = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #4
finger = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=90) #3
unterArm = AngularServo(19, min_angle=90, max_angle=-90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #2
oberArm = AngularServo(5, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #1

@app.post("/move")
async def get_body(request: Request):
    if not request:
      return {"error": "Fehlendes JSON"}
    positions = await request.json()
    X = positions['col']
    Y = positions['row']
    goto(x=X, y=Y)
    sleep(1)
    down(getOffset(y=Y))
    sleep(1)
    up()
    sleep(0.5)
    reset()

@app.post("/end")
async def endGame(request: Request):
  if not request:
    return {"error": "Fehlendes JSON"}
  winner = await request.json()
  # TODO: print winner on MATRIX LED
  print(f"WINNER IS: {winner['winner']}")

@app.post("/movePerAngle")
async def endGame(request: Request):
  if not request:
    return {"error": "Fehlendes JSON"}
  angles = await request.json()
  gotoRaw(angles['ober'], angles['unter'], angles['finger'])
  sleep(1)
  down()
  sleep(1)
  up()
  sleep(0.5)
  reset()

# Mapping von reellen Feldern (x,y) auf 3er Paar von ausgemessenen Winkeln, für die Stellung der ServoMotoren
def getPositionAngles(x, y):
  return lookupTable[x][y]

# Mithilfe des Mapping ausgeführte Bewegung. Gehe zum Punkt X,Y
def goto(x, y):
  position = getPositionAngles(x, y)
  gotoRaw(position[0], position[1], position[2])

# Gehe zu Oberarm, Unterarm und Finger Winkel
def gotoRaw(ober, unter, fing):
  oberArm.angle = ober
  unterArm.angle = unter
  finger.angle = fing

# Stift senken
def down(offset=0):
  stift.angle = -27 - offset

# Stift heben
def up():
  stift.angle = -90

def getOffset(y):
  return -0.75 * (6 - y)

# Ausgangsposition
def reset():
  oberArm.angle = -90
  unterArm.angle = -90
  finger.angle = 90
  stift.angle = -90