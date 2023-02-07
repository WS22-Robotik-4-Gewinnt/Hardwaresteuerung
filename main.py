import threading
import json

from gpiozero import AngularServo, Button, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from fastapi import FastAPI, Request
from pydantic import BaseModel
from time import sleep, strftime
from datetime import datetime
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
import json
import requests

import logging

# logging
LOG = "logging_data.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)

diffi = 1
readyButton = Button(21)
difficultyButton = Button(26)

dict = {
  1: 'Kids',
  2: 'Leicht',
  3: 'Mittel',
  4: 'Schwer',
  5: '42'
}

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=8)


class Positions(BaseModel):
  col: int
  row: int


class Winner(BaseModel):
  winner: str

# Thread for Difficulty
def diffi_Thread():
  global diffi
  t = threading.currentThread()
  print("THREAD RUNNING")
  while getattr(t, "run", True):
    try:
      if readyButton.is_pressed:
        difficulty = '{"difficulty": ' + str(diffi) + '}'
        difficulty = json.loads(difficulty)
        requests.post("http://localhost:8090/ready", json=difficulty)
        sleep(1)
      if difficultyButton.is_pressed:
        diffi += 1
        if diffi > 5:
          diffi = 1
        sleep(0.5)
      with canvas(virtual) as draw:
        text(draw, (0, 1), dict.get(diffi), fill="white", font=proportional(LCD_FONT))

    except KeyboardInterrupt:
      GPIO.cleanup()
  print("THREAD STOPPED")



difficultyThread = threading.Thread(target=diffi_Thread, args=[])
difficultyThread.start()


Device.pin_factory = PiGPIOFactory()
app = FastAPI()

lookupTable = [[[-20, 55, 2], [-37, 80, -2], [-50, 85, 23], [-59, 86, 43], [-64, 87, 60], [-68, 87, 75]],
               [[-32, 58, 10], [-48, 80, 12], [-61, 85, 32], [-69, 86, 50], [-77, 87, 66], [-83, 88, 80]],
               [[-40, 62, 10], [-57, 80, 17], [-70, 85, 36], [-80, 86, 54], [-83, 78, 78], [-90, 80, 90]],
               [[42, -26, -40], [53, -36, -52], [64, -48, -60], [77, -60, -65], [90, -72, -72], [90, -65, -90]],
               [[48, -65, -5], [64, -80, -14], [75, -86, -30], [82, -86, -44], [85, -80, -64], [86, -76, -81]],
               [[41, -65, 0], [55, -80, -10], [66, -85, -26], [73, -86, -41], [77, -85, -57], [83, -89, -68]],
               [[30, -58, 0], [47, -80, -4], [56, -85, -20], [63, -86, -37], [66, -84, -53], [68, -85, -65]]]

stift = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0024,
                     initial_angle=-90)  # 4
finger = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0024,
                      initial_angle=90)  # 3
unterArm = AngularServo(19, min_angle=90, max_angle=-90, min_pulse_width=0.0006, max_pulse_width=0.0024,
                        initial_angle=-90)  # 2
oberArm = AngularServo(5, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0024,
                       initial_angle=-90)  # 1


@app.post("/move")
async def move(positions: Positions):
  goto(x=positions.col, y=positions.row)
  sleep(1)
  down(getOffset(y=positions.row))
  sleep(1)
  wiggle(finger.angle)
  sleep(1)
  up()
  sleep(0.5)
  reset()


@app.post("/end")
def endGame(winner: Winner):
  global difficultyThread
  print("STOP THREAD")
  difficultyThread.run = False
  with canvas(virtual) as draw:
    text(draw, (0, 1), "jkhksdbufi", fill="white", font=proportional(LCD_FONT))
  sleep(3)
  difficultyThread.run = True


@app.post("/movePerAngle")
async def movePerAngle(request: Request):
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


def wiggle(fingerAngle: int):
  if fingerAngle <= 82:
    finger.angle = fingerAngle + 8
    sleep(1)
  else:
    finger.angle = 90

  if fingerAngle >= -85:
    finger.angle = fingerAngle - 5
  else:
    finger.angle = -90