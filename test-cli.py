import sys
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

reset()
sleep(1.5)

oberArm.angle = float(sys.argv[1])-4
unterArm.angle = float(sys.argv[2])+2
finger.angle = float(sys.argv[3])
sleep(1.5)
stift.angle = -32
sleep(1)
stift.angle = -90
sleep(1)
gpio.cleanup()

sleep(0.5)
