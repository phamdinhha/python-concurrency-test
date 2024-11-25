import time
import asyncio
import requests
import aiohttp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

URLS = [
    'https://api.github.com/events',
    'https://api.github.com/emojis',
    'https://api.github.com/meta',
    'https://api.github.com/feeds',
] * 5

def fetch_url(url):
    try:
        response = requests.get(url, timeout=30)
        return len(response.content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return 0

async def async_fetch_url(session, url):
    try:
        async with session.get(url) as response:
            content = await response.read()
            return len(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return 0

def run_sequential():
    start_time = time.time()
    results = []
    
    for url in URLS:
        results.append(fetch_url(url))
    
    end_time = time.time()
    print(f"Sequential: {end_time - start_time:.2f} seconds")
    return sum(results)

def run_multiprocessing(num_processes=4):
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(fetch_url, URLS))
    
    end_time = time.time()
    print(f"Multiprocessing ({num_processes} processes): {end_time - start_time:.2f} seconds")
    return sum(results)

def run_multithreading(num_threads=20):  # More threads for I/O bound tasks
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(fetch_url, URLS))
    
    end_time = time.time()
    print(f"Multithreading ({num_threads} threads): {end_time - start_time:.2f} seconds")
    return sum(results)

async def run_asyncio():
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch_url(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Asyncio ({len(URLS)} tasks): {end_time - start_time:.2f} seconds")
    return sum(results)

if __name__ == "__main__":
    print("Running I/O-bound benchmarks...\n")
    
    # Sequential
    seq_result = run_sequential()
    
    # Multiprocessing
    mp_result = run_multiprocessing()
    
    # Multithreading
    mt_result = run_multithreading()
    
    # Asyncio
    asyncio_result = asyncio.run(run_asyncio())
    
    print("\nVerification - All approaches received same amount of data:", 
          seq_result == mp_result == mt_result == asyncio_result)
    print(f"Total data received: {seq_result:,} bytes")