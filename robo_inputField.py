from gpiozero import AngularServo, Button
from time import sleep
import random

lookupTable = [[[-25, 55, 5], [-42, 85, -5], [-53, 85, 22], [-61, 86, 42], [-66, 87, 57], [-68, 87, 71]],
               [[-35, 60, 5], [-52, 85, 4], [-64, 85, 32], [-72, 86, 49], [-77, 87, 63], [-83, 88, 77]],
               [[-45, 65, 7], [-61, 85, 9], [-72, 85, 34], [-82, 86, 52], [-83, 79, 73], [-86, 75, 90]],
               [[38, -24, -44], [51, -36, -53], [64, -48, -63], [77, -60, -68], [90, -72, -73], [90, -68, -90]],
               [[45, -65, -3], [62, -85, -7], [74, -85, -33], [82, -86, -49], [85, -80, -68], [86, -75, -84]],
               [[35, -60, 2], [52, -85, -1], [64, -85, -30], [72, -86, -45], [77, -87, -58], [83, -88, -71]],
               [[25, -55, -2], [42, -85, 5], [54, -85, -22], [61, -86, -39], [66, -87, -52], [68, -87, -65]]]

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

