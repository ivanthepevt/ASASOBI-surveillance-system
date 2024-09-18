import cv2
import numpy as np

class ImageProcessor:
  def process(self, raw_data):
    # Convert sensor data to image format
    if raw_data is not None:
      # Resize the image to 1366x768
      resized_image = cv2.resize(raw_data, (1366, 768))
      return resized_image
    else:
      return None