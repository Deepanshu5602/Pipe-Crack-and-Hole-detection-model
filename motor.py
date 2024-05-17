import RPi.GPIO as GPIO
import time

# Define GPIO pins for motor control
motor1_in1 = 17
motor1_in2 = 22

motor2_in1 = 23
motor2_in2 = 24

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup motor control pins as outputs
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)

GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)

try:
    # Move motors forward continuously
    GPIO.output(motor1_in1, GPIO.HIGH)
    GPIO.output(motor1_in2, GPIO.LOW)

    GPIO.output(motor2_in1, GPIO.HIGH)
    GPIO.output(motor2_in2, GPIO.LOW)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Stop motors and cleanup GPIO
    GPIO.cleanup()
