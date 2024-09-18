
# ASASOBI: Privacy-Preserving Digital Twin Surveillance System

**ASASOBI** is a privacy-preserving digital twin surveillance system that processes data from IoT sensors (such as LiDAR and radar) or conventional cameras. The system creates anonymized real-time 3D models in a virtual environment using **UC-win/Road**, while ensuring no identifiable personal information is streamed or stored. All data is processed locally, and only anonymized data is transmitted.

---

## **System Overview**

- **Radar Support**: Currently supports **Ultrasonic HC-SR04** sensor.
- **LiDAR Support**: Any LiDAR sensor with a **USB interface** can connect to the system.
- **Camera Support**: Any conventional cameras work.

Once the system is running, a **WebSocket server** will be hosted, ready to send real-time data to **UC-win/Road** for visualization. This enables creating a digital twin of the monitored environment, using anonymized data from sensors.

## **Installation Guide**

### **Step 1: Clone the Repository**

Start by cloning the ASASOBI project repository to your local machine.

```bash
git clone https://github.com/ivanthepevt/ASASOBI-surveillance-system
cd ASASOBI-surveillance-system
```

### **Step 2: Install Dependencies**

Ensure you have Python 3.8 or later installed. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### **Step 3: Set Up the Configuration**

Before running the system, configure the environment variables in `config.py`.

1. **API_KEY**: Replace `'your-openai-api-key'` with your actual OpenAI API key.
2. **WEBSOCKET_PORT**: Set the port for the WebSocket server (default is `8765`).
3. **SENSOR_TYPE**: Set the type of sensor you're using. Options:
   - `'camera'`
   - `'lidar'`
   - `'radar'` (Only supports **Ultrasonic HC-SR04** sensor currently)

You can rename the example configuration file and update the necessary fields:

```bash
cp config.py.example config.py
```

### **Step 4: Connect Your Sensors**

- **Ultrasonic HC-SR04 Radar Sensor**: Ensure the sensor is correctly connected to your Raspberry Pi or compatible device via GPIO pins. Follow standard GPIO setup for HC-SR04.
  
- **LiDAR Sensor**: Any LiDAR with a **USB interface** can be connected. Ensure drivers are installed and the device is accessible as a USB serial device on the system.

### **Step 5: Run the System**

After configuring everything, run the system using:

```bash
python src/main.py
```

This command will:
1. Start the sensor data capture.
2. Process sensor data into images.
3. Use GPT-4 with vision capabilities to extract metadata.
4. Stream anonymized JSON data through a **WebSocket server** to be consumed by **UC-win/Road** for visualization.

---

## **Configuration Variables**

All environment variables are stored in `config.py`. Here’s an example of how to configure it:

```python
# config.py example

API_KEY = 'your-openai-api-key'  # OpenAI GPT-4-o-mini API key
WEBSOCKET_PORT = 8765  # Port for WebSocket server
SENSOR_TYPE = 'lidar'  # Options: 'camera', 'lidar', 'radar'
UC_WIN_ROAD_WS_URL = 'ws://localhost:8765'  # WebSocket URL for UC-win/Road
```

You can modify the `config.py` file to change sensor types, WebSocket ports, and API keys easily.

---

## **How the System Works**

### **Step 1: Data Capture**

- **Cameras**: Capture video frames and process them locally into anonymized metadata.
- **LiDAR**: Captures point cloud data via USB and converts it into image format for further processing.
- **Radar**: Captures distance and proximity data using **HC-SR04**, converts it into an image for processing.

### **Step 2: Local Processing**

The sensor data is processed using a **Python-based local processing unit**. The data is converted into an image format, and **GPT-4-o-mini with vision capabilities** is called to analyze the image and output metadata (e.g., object types, positions) in **JSON format**.

### **Step 3: Anonymized Data Transmission**

The processed metadata (in JSON format) is transmitted via a **WebSocket server** to the configured WebSocket endpoint (`ws://localhost:8765`). The data includes object positions, movements, and types, with no identifiable personal information.

### **Step 4: UC-win/Road Visualization**

The anonymized JSON data can be integrated with **UC-win/Road** for real-time visualization in a digital twin environment. The 3D models in UC-win/Road will reflect the real-time data captured from your sensors.

---

## **Key Features**

- **Privacy-Preserving**: No raw video streams are transmitted. All processing is done locally, and only anonymized metadata is sent over the network.
- **Multi-Sensor Support**: Compatible with cameras, LiDAR sensors (via USB), and the **HC-SR04 ultrasonic radar sensor**.
- **GPT-4 Vision Integration**: Uses GPT-4's vision API to analyze images and produce structured metadata in JSON format.
- **Real-Time Data Transmission**: Streams data over a WebSocket server to be consumed by UC-win/Road for real-time 3D visualization.
- **Modular Design**: Easily extendable for additional sensor types or use cases.

---

## **Dependencies**

The system requires the following Python packages, listed in `requirements.txt`:

```txt
opencv-python
websockets
openai
numpy
```

To install these dependencies, simply run:

```bash
pip install -r requirements.txt
```

---

## **Running the System**

After installing dependencies and configuring environment variables, run the system:

```bash
python src/main.py
```

This will start the WebSocket server and stream anonymized data ready for visualization in UC-win/Road.

---

## **Connecting to UC-win/Road**

Once the system is running, the processed JSON data will be streamed to the WebSocket endpoint (`ws://localhost:8765`). You can configure UC-win/Road to connect to this WebSocket for real-time visualization of the sensor data as anonymized 3D models in the virtual environment.


### **Support**

For any issues or questions, feel free to open an issue on GitHub or contact the project maintainers.

---

This `README.md` now serves as the full instruction guide for setting up, configuring, and using ASASOBI. You can upload this codebase and documentation directly to GitHub or any other repository for easy deployment and user access. Let me know if you need any additional modifications!