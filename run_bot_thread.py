import io
import logging
import socketserver
from http import server
from threading import Condition, Thread
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

# Motor 1
motor1_pwm_pin = 12
motor1_dir_pin1 = 5
motor1_dir_pin2 = 6

# Motor 2
motor2_pwm_pin = 16
motor2_dir_pin1 = 13
motor2_dir_pin2 = 26

# Set up GPIO pins for motor control
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
    time.sleep(t)
    stop()


def stop():
    GPIO.output(motor1_dir_pin1, GPIO.LOW)
    GPIO.output(motor1_dir_pin2, GPIO.LOW)
    GPIO.output(motor2_dir_pin1, GPIO.LOW)
    GPIO.output(motor2_dir_pin2, GPIO.LOW)
    motor1_pwm.ChangeDutyCycle(0)
    motor2_pwm.ChangeDutyCycle(0)


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def run_bot():
    while True:
        try:
            forward(2)
        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()


if __name__ == "__main__":
    PAGE = """\
    <html>
    <head>
    <title>Live Stream Pipe Robot</title>
    </head>
    <body>
    <center> <h1>Live Stream Pipe Robot</h1> </center>
    <img src="stream.mjpg" width="1600" height="768" />
    </body>
    </html>
    """

    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (1280, 1024)}))
    output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        bot_thread = Thread(target=run_bot)
        bot_thread.start()

        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()

    finally:
        stop()
        picam2.stop_recording()
        bot_thread.join()
