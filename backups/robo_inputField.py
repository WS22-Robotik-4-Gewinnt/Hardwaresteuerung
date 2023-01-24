from gpiozero import AngularServo, Button, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import random

Device.pin_factory = PiGPIOFactory()

lookupTable = [[[-20, 55, 2], [-37, 80, -2], [-50, 85, 23], [-59, 86, 43], [-64, 87,60], [-68, 87, 75]],
               [[-32, 58, 10], [-48, 80, 12], [-61, 85, 32], [-69, 86, 50], [-77, 87, 66], [-83, 88, 80]],
               [[-40, 62, 10], [-57, 80, 17], [-70, 85, 36], [-80, 86, 54], [-83, 78, 78], [-90, 80, 90]],
               [[42, -26, -40], [53, -36, -52], [64, -48, -60], [77, -60, -65], [90, -72, -72], [90, -65, -90]],
               [[48, -65, -5], [64, -80, -14], [75, -86, -30], [82, -86, -44], [85, -80, -64], [86, -76, -81]],
               [[41, -65, 0], [55, -80, -10], [66, -85, -26], [73, -86, -41], [77, -85, -57], [83, -89, -68]],
               [[30, -58, 0], [47, -80, -4], [56, -85, -20], [63, -86, -37], [66, -84, -53], [68, -85, -65]]]

stift = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) 	#4
finger = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=90) 	#3
unterArm = AngularServo(19, min_angle=90, max_angle=-90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) 	#2
oberArm = AngularServo(5, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90) 	#1

btn = Button(14)

# Ausgangsposition
def reset():
  oberArm.angle = -90
  unterArm.angle = -90
  finger.angle = 90
  stift.angle = -90

# Gehe zu Oberarm, Unterarm und Finger Winkel
def gotoRaw(ober, unter, fing):
  oberArm.angle = ober
  unterArm.angle = unter
  finger.angle = fing

# Stift senken
def down(offset = 0):
  stift.angle = -33 - offset

# Stift heben
def up():
  stift.angle = -90

# Mapping von reellen Feldern (x,y) auf 3er Paar von ausgemessenen Winkeln, für die Stellung der ServoMotoren
def getPositionAngles(x, y):
  return lookupTable[x][y]

# Mithilfe des Mapping ausgeführte Bewegung. Gehe zum Punkt X,Y
def goto(x, y):
  position = getPositionAngles(x,y)
  gotoRaw(position[0]-4, position[1]+2, position[2])

# TODO noch nicht funktional
def drawLine(fromX, fromY, toX, toY):
  goto(fromX, fromY)
  sleep(1.0)
  down()
  sleep(0.5)

  fromPos = getPositionAngles(fromX, fromY)
  destPos = getPositionAngles(toX, toY)

  for x in range(toX - fromX):
    for y in range(toY - fromY):
      goto(fromX + x, fromY + y)
      sleep(0.5)

# Offset für den Stift. Die Platte ist uneben zu der Halterung der Servo Motoren. Durch die vorher angegebene Konstante im Projekt drückt der Stift sonst immer zu stark auf.
# Deshalb berechnet die Funktion den genauen Winkel, bzw. Druck der auf die Stiftspitze wirkt, damit nicht nach 100 mal zeichnen die Spitze so stark eingedrückt ist, dass sie nur noch auf einer Seite zeichen kann.
def getOffset(y):
  return -0.75 * (6-y)

# Hilfs-Routine zum Testen der Bewegung, nicht zyklisch!
def gotoRandom():
  x = random.randrange(0, 7)
  y = random.randrange(0, 6)
  goto(x, y)

  sleep(1)
  # Stift senken mit Offset, da sonst der Stift kaputt geht umso weiter weg er sich bewegt.. Keine Ahnung warum
  return [x,y]


while True:
  # Initial Anfahren auf Startposition
  reset()
  sleep(1.5)

  #input dialog: catch index out of bounds
  inputX = -1
  inputY = -1
  while(inputX < 0 or inputY < 0 or inputX > 6 or inputY > 5):

    print("x: ")
    inputX = int(input())
    print("y: ")
    inputY = int(input())

    if(inputX < 0 or inputY < 0):
	    print("Fieldindex cannot be negative. Repeat Input")
    if(inputX > 6 or inputY > 5):
	    print("Fieldindex out of bounds. Repeat Input")

  print("going to [" + str(inputX) + "," + str(inputY) + "]")

  #button freigabe
  print("Press button when ready")
  btn.wait_for_press()

  #move
  goto(inputX, inputY)
  sleep(1.5)

  #draw
  down(getOffset(inputY))
  sleep(0.25)
  up()
  sleep(0.5)

# Sollte nie erreicht werden, dennoch nach Absturz ggf. Ausgangsposition probieren wiederherzustellen.
reset()
sleep(1.5)

