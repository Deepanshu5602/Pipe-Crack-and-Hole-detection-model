import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the sensor
TRIG_PIN = 23
ECHO_PIN = 24

# Set up the GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Ensure the trigger pin is low
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    # Generate a pulse on the trigger pin
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Record the time when the pulse is sent
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()

    # Record the time when the echo is received
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end_time - pulse_start_time

    # Speed of sound is approximately 343 meters/second (or 34300 centimeters/second)
    # Distance = (time taken for pulse to travel from sensor to object and back) / 2
    distance = (pulse_duration * 34300) / 2

    return distance

# Initialize lists to store time and distance data
distances = []
distance_travelled = []
speed = 10  # Speed of the car in cm/s
initial_time = time.time()

try:
    while True:
        # Measure the distance
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        # Get the current time
        current_time = time.time()
        distance_car = speed * (current_time - initial_time)

        # Add data to lists
        distance_travelled.append(distance_car)
        distances.append(distance)

        # Wait for a short time before the next measurement
        time.sleep(0.01)

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()

    # Set up the plot
    plt.plot(distance_travelled, distances)
    plt.title('Distance Travelled vs Cross-Sectional Distance')
    plt.xlabel('Distance by Car(cm)')
    plt.ylabel('Cross-Sectional Distance (cm)')
    plt.grid(True)

    # Get the timestamp for the filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save the graph as an image with the timestamp as the filename
    plt.savefig(f'distance_plot_{timestamp}.png')

    # Close the plot
    plt.close()
