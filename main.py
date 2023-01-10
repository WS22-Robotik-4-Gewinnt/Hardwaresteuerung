from gpiozero import AngularServo, Button
from time import sleep
from fastapi import FastAPI, Request
app = FastAPI()

lookupTable = [[[-25, 55, 5], [-42, 85, -5], [-53, 85, 22], [-61, 86, 42], [-66, 87, 57], [-68, 87, 71]],
               [[-35, 60, 5], [-52, 85, 4], [-64, 85, 32], [-72, 86, 49], [-77, 87, 63], [-83, 88, 77]],
               [[-45, 65, 7], [-61, 85, 9], [-72, 85, 34], [-82, 86, 52], [-83, 79, 73], [-86, 75, 90]],
               [[38, -24, -44], [51, -36, -53], [64, -48, -63], [77, -60, -68], [90, -72, -73], [90, -68, -90]],
               [[45, -65, -3], [62, -85, -7], [74, -85, -33], [82, -86, -49], [85, -80, -68], [86, -75, -84]],
               [[35, -60, 2], [52, -85, -1], [64, -85, -30], [72, -86, -45], [77, -87, -58], [83, -88, -71]],
               [[25, -55, -2], [42, -85, 5], [54, -85, -22], [61, -86, -39], [66, -87, -52], [68, -87, -65]]]

stift = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #4
finger = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=90) #3
unterArm = AngularServo(19, min_angle=90, max_angle=-90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #2
oberArm = AngularServo(5, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) #1

@app.post("/move")
async def get_body(request: Request):
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

# Mapping von reellen Feldern (x,y) auf 3er Paar von ausgemessenen Winkeln, für die Stellung der ServoMotoren
def getPositionAngles(x, y):
  return lookupTable[x][y]


# Mithilfe des Mapping ausgeführte Bewegung. Gehe zum Punkt X,Y
def goto(x, y):
  position = getPositionAngles(x, y)
  gotoRaw(position[0] - 4, position[1] + 2, position[2])

# Gehe zu Oberarm, Unterarm und Finger Winkel
def gotoRaw(ober, unter, fing):
  oberArm.angle = ober
  unterArm.angle = unter
  finger.angle = fing

# Stift senken
def down(offset=0):
  stift.angle = -33 - offset

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

