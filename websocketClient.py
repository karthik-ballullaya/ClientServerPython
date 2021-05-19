import asyncio
import websockets

async def send_message():
  url = "ws://localhost:8000"
  message = input("Enter your message to the server: ")
  async with websockets.connect(url) as websocket:
    await websocket.send(message)

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  try:
    while True:
      loop.run_until_complete(send_message())
  except KeyboardInterrupt as e:
    print("\nExiting program")
    loop.close()