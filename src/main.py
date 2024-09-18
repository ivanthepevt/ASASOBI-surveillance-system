import asyncio
from sensor_interface import SensorInterface
from image_processor import ImageProcessor
from ai_processor import AIProcessor
from websocket_server import WebSocketServer
from config import WEBSOCKET_PORT

async def main():
    # Initialize components
    sensor = SensorInterface()
    image_processor = ImageProcessor()
    ai_processor = AIProcessor()
    websocket_server = WebSocketServer()

    # Start WebSocket server
    asyncio.create_task(websocket_server.start_server())

    while True:
        #Capture Data and convert to image
        raw_data = sensor.capture_data()
        image = image_processor.process(raw_data)
        json_data = ai_processor.process_image(image)

        #Send Data via WebSocket
        await websocket_server.send_data(json_data)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
