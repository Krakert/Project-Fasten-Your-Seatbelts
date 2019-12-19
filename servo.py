
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SERVO_CHANNEL = 16

GPIO.setup(SERVO_CHANNEL, GPIO.OUT)
p = GPIO.PWM(SERVO_CHANNEL, 50)

def set_board_to_center():
  CENTER = 60
  global current_position
  current_position = CENTER
  p.start((CENTER/10))
  time.sleep(2)
 
def rotate_board(direction):
  global current_position
  LEFT_MAX = 115
  RIGHT_MAX = 25
  DELAY = 0.25
  if direction == 1:
    current_position = current_position + 1
    if current_position > LEFT_MAX:
      current_position = LEFT_MAX
    time.sleep(DELAY)

  elif direction == 2:
    current_position = current_position - 1
    if current_position < RIGHT_MAX:
      current_position = RIGHT_MAX
    time.sleep(DELAY)
  print(current_position)
  p.ChangeDutyCycle((current_position/10))
 