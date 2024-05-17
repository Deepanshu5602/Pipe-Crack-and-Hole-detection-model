import RPi.GPIO as GPIO
import time

class OpticalEncoder:
    def __init__(self, pulses_per_revolution):
        self.pulses_per_revolution = pulses_per_revolution
        self.total_pulses = 0

    def update(self, channel):
        self.total_pulses += 1

    def reset(self):
        self.total_pulses = 0

    def distance_covered(self, wheel_radius):
        # Calculate distance covered using total pulses and wheel circumference
        wheel_circumference = 2 * 3.14159 * wheel_radius
        total_distance = (self.total_pulses / self.pulses_per_revolution) * wheel_circumference
        return total_distance

# Setup GPIO
GPIO.setmode(GPIO.BCM)
encoder_pin = 17  # Example GPIO pin, adjust as needed
GPIO.setup(encoder_pin, GPIO.IN)

# Example wheel parameters
pulses_per_revolution = 20
wheel_radius = 0.22  # in meters (adjust as per your bot's wheel size)

# Create encoder object
encoder = OpticalEncoder(pulses_per_revolution)

# Define callback function
def pulse_callback(channel):
    encoder.update(channel)

# Add event detection
GPIO.add_event_detect(encoder_pin, GPIO.RISING, callback=pulse_callback)

try:
    while True:
        # Your main program loop can go here
        # For example, you might control motors and do other tasks
        time.sleep(1)  # Just to keep the program running
        
        # Calculate and print distance covered periodically
        distance = encoder.distance_covered(wheel_radius)
        print("Distance covered:", distance*100, "cm")

except KeyboardInterrupt:
    GPIO.cleanup()
