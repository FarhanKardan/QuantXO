
import asyncio
import json
import websockets
import ssl
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models import TickData

class BitmexWebSocket:
    def __init__(self, testnet=False):
        self.ws_url = "wss://testnet.bitmex.com/realtime" if testnet else "wss://ws.bitmex.com/realtime"
        self.websocket = None
    
    async def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        self.websocket = await asyncio.wait_for(
            websockets.connect(self.ws_url, ssl=ssl_context),
            timeout=10
        )
        print(f"Connected to Bitmex WebSocket: {self.ws_url}")
    
    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            print("Disconnected from Bitmex WebSocket")
    

    
    async def ticks(self, symbol):
        await self.connect()
        subscribe_message = {
            "op": "subscribe",
            "args": [f"trade:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            data = json.loads(message)
            if 'table' in data and data['table'] == 'trade' and 'data' in data:
                return [
                    TickData(
                        symbol=trade.get('symbol', ''),
                        side=trade.get('side', ''),
                        size=float(trade.get('size', 0)),
                        price=float(trade.get('price', 0)),
                        timestamp=datetime.strptime(trade.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                    for trade in data['data']
                ]
    
    async def stream_ticks(self, symbol, duration_seconds=60):
        """Stream ticks for a specified duration"""
        await self.connect()
        subscribe_message = {
            "op": "subscribe",
            "args": [f"trade:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        print(f"Started streaming ticks for {symbol}")
        
        start_time = datetime.now()
        tick_count = 0
        
        try:
            async for message in self.websocket:
                # Check if duration exceeded
                if (datetime.now() - start_time).total_seconds() > duration_seconds:
                    break
                
                try:
                    data = json.loads(message)
                    
                    if 'table' in data and data['table'] == 'trade' and 'data' in data:
                        for trade in data['data']:
                            try:
                                timestamp = datetime.strptime(trade.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                                tick_data = TickData(
                                    symbol=trade.get('symbol', symbol),
                                    side=trade.get('side', ''),
                                    size=float(trade.get('size', 0)),
                                    price=float(trade.get('price', 0)),
                                    timestamp=timestamp
                                )
                                
                                tick_count += 1
                                print(f"Tick {tick_count}: {tick_data.symbol} {tick_data.side} {tick_data.price} {tick_data.size}")
                                
                            except (ValueError, TypeError) as e:
                                print(f"Error parsing trade: {e}")
                                continue
                    
                    elif 'info' in data:
                        print(f"Info: {data['info']}")
                    elif 'error' in data:
                        print(f"Error: {data['error']}")
                        
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            print(f"Error in stream: {e}")
        finally:
            await self.disconnect()
            print(f"Stream completed. Total ticks: {tick_count}")

async def main():
    bitmex_ws = BitmexWebSocket(testnet=False)
    
    # Test tick streaming
    await bitmex_ws.stream_ticks("XBTUSD")

if __name__ == "__main__":
    asyncio.run(main()) 
