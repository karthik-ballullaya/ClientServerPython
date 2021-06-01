import asyncio
import websockets

async def message_handler(websocket, path):
  ip_addr, port_id, *_ = websocket.remote_address
  message = await websocket.recv()
  print(f'>{ip_addr}:{port_id} - {message}')
  await websocket.send('Received message')

start_server = websockets.serve(message_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()