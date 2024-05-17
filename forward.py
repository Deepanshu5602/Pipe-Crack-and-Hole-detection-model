import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard
import sys


# Set the GPIO mode and pins for motor control
GPIO.setmode(GPIO.BCM)

# Motor 1
motor1_pwm_pin = 12
motor1_dir_pin1 = 6
motor1_dir_pin2 = 5

# Motor 2
motor2_pwm_pin = 16
motor2_dir_pin1 = 13
motor2_dir_pin2 = 26

# Set up GPIO pins
GPIO.setup(motor1_pwm_pin, GPIO.OUT)
GPIO.setup(motor1_dir_pin1, GPIO.OUT)
GPIO.setup(motor1_dir_pin2, GPIO.OUT)

GPIO.setup(motor2_pwm_pin, GPIO.OUT)
GPIO.setup(motor2_dir_pin1, GPIO.OUT)
GPIO.setup(motor2_dir_pin2, GPIO.OUT)

# Create PWM instances for motor control
motor1_pwm = GPIO.PWM(motor1_pwm_pin, 100)  # 100 Hz frequency
motor2_pwm = GPIO.PWM(motor2_pwm_pin, 100)

# Initialize PWM with 0% duty cycle (stopped)
motor1_pwm.start(0)
motor2_pwm.start(0)


def forward(t):
    motor1_pwm.ChangeDutyCycle(60)
    motor2_pwm.ChangeDutyCycle(60)
    GPIO.output(motor1_dir_pin1, GPIO.HIGH)
    GPIO.output(motor1_dir_pin2, GPIO.LOW)
    GPIO.output(motor2_dir_pin1, GPIO.HIGH)
    GPIO.output(motor2_dir_pin2, GPIO.LOW)

def stop():
    GPIO.output(motor1_dir_pin1, GPIO.LOW)
    GPIO.output(motor1_dir_pin2, GPIO.LOW)
    GPIO.output(motor2_dir_pin1, GPIO.LOW)
    GPIO.output(motor2_dir_pin2, GPIO.LOW)
    motor1_pwm.ChangeDutyCycle(0)
    motor2_pwm.ChangeDutyCycle(0)

def press(key):
    print(key)
    if key=='q':
        stop()
        GPIO.cleanup()
        sys.exit()

while True:
    try:
        forward(2)     
        listen_keyboard(on_press=press)  
    except KeyboardInterrupt or 0xFF == ord('q'):
        stop()
        GPIO.cleanup()