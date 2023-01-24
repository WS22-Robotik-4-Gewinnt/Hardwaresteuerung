from gpiozero import AngularServo, Button, Device
#from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

#lookupTable = [{{-10, 5, 37}, {-20, 5, 45}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}},
#               {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}}
#               ]


#factory = PiGPIOFactory()
#factory = NativeFactory()

stift = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90)
finger = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=90)
unterArm = AngularServo(19, min_angle=90, max_angle=-90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90)
oberArm = AngularServo(5, min_angle=-90, max_angle=90, min_pulse_width=0.0006, max_pulse_width= 0.0024, initial_angle=-90)

btn = Button(14)

def reset():
  oberArm.angle = -90
  unterArm.angle = -90
  finger.angle = 90
  stift.angle = -90

# Gehe zu Oberarm, Unterarm und Finger Winkel
def goto(ober, unter, fing):
  oberArm.angle = ober
  unterArm.angle = unter
  finger.angle = fing

# Stift senken
def down():
  stift.angle = -30

# Stift heben
def up():
  stift.angle = -90

while True:
  print('o')
  oberArm.angle = input()
  print('u')
  unterArm.angle = input()
  print('f')
  finger.angle = input()
  sleep(0.5)
  down()
  sleep(1.5)
  up()
  sleep(0.25)
  reset()
