import asyncio
import websockets

async def message_handler(websocket, path):
  message = await websocket.recv()
  print(f'> {message}')

start_server = websockets.serve(message_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()