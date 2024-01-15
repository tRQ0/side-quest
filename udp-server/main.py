import asyncio
import websockets

async def handle_websocket(websocket, path):
    while True:
        # Receive data from the WebSocket client
        data = await websocket.recv()
        print(f"Received data from client: {data}")
        
        # Send a response back to the client
        if data == 'Hello, server! How are you?':
            response = 'Received your message, client!'
            await websocket.send(response)

        if data == 'see':
            await websocket.send('YES!')
        await websocket.send('alive!')

# Start the WebSocket server
start_server = websockets.serve(handle_websocket, "127.0.0.1", 81)

# Run the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
 
