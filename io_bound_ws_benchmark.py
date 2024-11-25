import time
import asyncio
import websockets
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from websockets.sync.client import connect as sync_connect
from websockets.client import connect as async_connect

# Using a public WebSocket echo server
WS_URL = "wss://ws.postman-echo.com/raw"
MESSAGE = "Hello, World!"
NUM_MESSAGES = 100  # Number of messages per connection
NUM_CONNECTIONS = 10  # Number of simultaneous connections

def sync_websocket_task():
    try:
        with sync_connect(WS_URL) as websocket:
            messages_received = 0
            for _ in range(NUM_MESSAGES):
                websocket.send(MESSAGE)
                response = websocket.recv()
                if response == MESSAGE:
                    messages_received += 1
            return messages_received
    except Exception as e:
        print(f"Error in sync websocket: {e}")
        return 0

async def async_websocket_task():
    try:
        websocket = await async_connect(WS_URL)
        messages_received = 0
        try:
            for _ in range(NUM_MESSAGES):
                await websocket.send(MESSAGE)
                response = await websocket.recv()
                if response == MESSAGE:
                    messages_received += 1
            return messages_received
        finally:
            await websocket.close()
    except Exception as e:
        print(f"Error in async websocket: {e}")
        return 0

def run_sequential():
    start_time = time.time()
    total_messages = 0
    
    for _ in range(NUM_CONNECTIONS):
        total_messages += sync_websocket_task()
    
    end_time = time.time()
    print(f"Sequential: {end_time - start_time:.2f} seconds")
    return total_messages

def run_multiprocessing(num_processes=4):
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Use submit() and create a list of futures
        futures = [executor.submit(sync_websocket_task) for _ in range(NUM_CONNECTIONS)]
        # Wait for all futures to complete and get results
        results = [f.result() for f in futures]
    
    end_time = time.time()
    print(f"Multiprocessing ({num_processes} processes): {end_time - start_time:.2f} seconds")
    return sum(results)

def run_multithreading(num_threads=10):
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Use submit() and create a list of futures
        futures = [executor.submit(sync_websocket_task) for _ in range(NUM_CONNECTIONS)]
        # Wait for all futures to complete and get results
        results = [f.result() for f in futures]
    
    end_time = time.time()
    print(f"Multithreading ({num_threads} threads): {end_time - start_time:.2f} seconds")
    return sum(results)

async def run_asyncio():
    start_time = time.time()
    
    # Create multiple WebSocket connections concurrently
    tasks = [async_websocket_task() for _ in range(NUM_CONNECTIONS)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Asyncio ({NUM_CONNECTIONS} connections): {end_time - start_time:.2f} seconds")
    return sum(results)

if __name__ == "__main__":
    print(f"Running WebSocket benchmarks...\n")
    print(f"Each connection will send/receive {NUM_MESSAGES} messages")
    print(f"Testing with {NUM_CONNECTIONS} simultaneous connections\n")
    
    # Install required packages
    # pip install websockets
    
    # Sequential
    seq_result = run_sequential()
    
    # Multiprocessing
    mp_result = run_multiprocessing()
    
    # Multithreading
    mt_result = run_multithreading()
    
    # Asyncio
    asyncio_result = asyncio.run(run_asyncio())
    
    print("\nVerification - Messages received by each approach:")
    print(f"Sequential: {seq_result}")
    print(f"Multiprocessing: {mp_result}")
    print(f"Multithreading: {mt_result}")
    print(f"Asyncio: {asyncio_result}")