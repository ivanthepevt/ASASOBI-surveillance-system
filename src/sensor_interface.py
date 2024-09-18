# Current radar only support untrasonic HC-SR04 sensor

import numpy as np
import cv2
import RPi.GPIO as GPIO
from config import SENSOR_TYPE
from rplidar import RPLidar

class SensorInterface:
  def __init__(self):
    if SENSOR_TYPE == 'camera':
      self.cap = cv2.VideoCapture(0)
    elif SENSOR_TYPE == 'lidar':
      self.lidar = RPLidar('/dev/ttyUSB0')  # lidar on port USB 0
    elif SENSOR_TYPE == 'radar':
      self.setup_radar()
    else:
      self.cap = None
      self.lidar_data = None
      self.radar_data = None

  def setup_radar(self):
    GPIO.setmode(GPIO.BOARD)
    self.PIN_TRIGGER = 7
    self.PIN_ECHO = 11
    GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(self.PIN_ECHO, GPIO.IN)
    GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

  def capture_data(self):
    if SENSOR_TYPE == 'camera':
      ret, frame = self.cap.read()
      if ret:
        return frame
      else:
        return None
    elif SENSOR_TYPE == 'lidar':
      return self.capture_lidar_data()
    elif SENSOR_TYPE == 'radar':
      return self.capture_radar_data()

  def capture_lidar_data(self):
    lidar_points = np.array([scan for scan in self.lidar.iter_scans()])
    image = self.lidar_to_image(lidar_points)
    return image

  def capture_radar_data(self):
    GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
    while GPIO.input(self.PIN_ECHO) == 0:
      pulse_start_time = time.time()
    while GPIO.input(self.PIN_ECHO) == 1:
      pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance

  def lidar_to_image(self, points):
    image = np.zeros((500, 500, 3), np.uint8)
    for point in points:
      x, y, z = int(point[0]), int(point[1]), int(point[2])
      cv2.circle(image, (x % 500, y % 500), 2, (0, 255, 0), -1) 
    return image

  def radar_to_image(self, distance):
    image = np.zeros((500, 500, 3), np.uint8)
    cv2.circle(image, (250, 250), int(distance), (255, 0, 0), 2)
    return image