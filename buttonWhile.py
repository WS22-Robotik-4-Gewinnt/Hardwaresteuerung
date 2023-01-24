import json
from gpiozero import Button
import requests

readyButton = Button(14)

while True:
  readyButton.wait_for_press()
  difficulty = '{"difficulty": 4}'
  difficulty = json.loads(difficulty)
  result = requests.post(f"http://localhost:8090/ready", json=difficulty)
  print("JSON SEND")