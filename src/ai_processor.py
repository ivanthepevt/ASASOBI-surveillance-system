import openai
import base64
import cv2
import numpy as np
import requests
from config import API_KEY

class AIProcessor:
  def process_image(self, image):
    if image is None:
      return None

    # Encode image to base64
    _, buffer = cv2.imencode('.jpg', image)
    img_str = base64.b64encode(buffer).decode('utf-8')

    # Prepare headers and payload for the API request
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
      "model": "gpt-4o-mini",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": """
                      You are a helpful observer. 
                      Observe what is in this frame, which can be a camera feed or a sensor visualization, and tell what you are seeing. 
                      Please provide your observations in the following JSON format:
                      {
                        "type": "person", // or "car", "bus", "truck"
                        "id": 2, // Unique ID assigned to each object from when it enters the frame until it exits
                        "position": { "x": 45, "y": 55, "z": 0 } // Coordinates from 0 to 100, indicating distance in meters
                      }
                      Please identify the type of object (person, car, bus, truck), assign a unique ID to each object from when it enters the frame until it exits, 
                      and provide the object's position in coordinates from 0 to 100, indicating distance in meters.
                      """
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{img_str}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    # Call GPT-4o with vision capabilities
    try:
      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      response.raise_for_status()
    except Exception as e:
      print(f"Error with GPT-4o Vision API: {e}")
      return None

    # Parse response
    json_data = response.json()
    if json_data:
      return json_data
    else:
      return None