from tradehub.websocket_client import DemexWebsocket
import asyncio


async def on_connect():
    print("I am connect to demex websocket!")
    await demex.subscribe_books("orderbook", "swth_eth1")


async def on_receive_message(message: dict):
    print("I received a message")
    print(message)


if __name__ == '__main__':
    demex: DemexWebsocket = DemexWebsocket('ws://164.132.169.19:5000/ws')
    asyncio.get_event_loop().run_until_complete(demex.connect(on_receive_message, on_connect))
