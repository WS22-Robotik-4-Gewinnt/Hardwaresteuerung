from gpiozero import Button
from time import sleep
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
import json
import requests

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=8)

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

while True:
  try:
    if readyButton.is_pressed:
      difficulty = '{"difficulty": ' + str(diffi) + '}'
      difficulty = json.loads(difficulty)
      result = requests.post("http://localhost:8090/ready", json=difficulty)
      print(f"JSON SEND + {difficulty}")
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
