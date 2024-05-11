import sys
import os
import asyncio
from aioconsole import get_standard_streams

LOCAL_HOST = '127.0.0.1'

class StdInWrapper:
  def __init__(self):
    self.loop = asyncio.get_event_loop()

  async def read(self, sz):
    data = await self.loop.run_in_executor(None, sys.stdin.readline)
    return data.encode()

class StdOutWrapper:
  def write(self, data):
    print(data.decode().replace('\r\n', '\n'), end='', flush=True)

  async def drain(self):
    pass

async def get_stdio():
  if os.name == 'nt':
    return StdInWrapper(), StdOutWrapper()
  else:
    return await get_standard_streams()

async def handle_reader(reader, writer):
  while True:
    data = await reader.read(4096)
    if not data or len(data) == 0:
      break
    writer.write(data)
    await writer.drain()
  for t in asyncio.all_tasks():
    if t is not asyncio.current_task():
      t.cancel()

async def server_main(sock_reader, sock_writer):
  stdin_reader, stdout_writer = await get_stdio()
  await asyncio.gather(
    handle_reader(stdin_reader, sock_writer),
    handle_reader(sock_reader, stdout_writer),
  )

async def main(port):
  server = await asyncio.start_server(server_main, LOCAL_HOST, port)
  try:
    async with server:
      await server.serve_forever()
  except:
    pass

if __name__ == "__main__":
  args = sys.argv
  if len(args) != 2:
    print('usage: python interactive_sock_proxy.py port')
    exit()
  try:
    asyncio.run(main(int(args[1])))
  except:
    pass
