import time
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def heavy_computation(n):
    results = []
    for i in range(n, n+3):
        results.append(fibonacci(i))
    return sum(results)

async def async_heavy_computation(n):
    return heavy_computation(n)

def run_sequential():
    start_time = time.time()
    for n in range(35, 39):
        heavy_computation(n)
    end_time = time.time()
    print(f"Sequential: {end_time - start_time:.2f} seconds")
    return 4

def run_multiprocessing(num_processes=4):
    start_time = time.time()
    numbers = list(range(35, 39))
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(heavy_computation, numbers))
    
    end_time = time.time()
    print(f"Multiprocessing ({num_processes} processes): {end_time - start_time:.2f} seconds")
    return len(results)

def run_multithreading(num_threads=4):
    start_time = time.time()
    numbers = list(range(35, 39))
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(heavy_computation, numbers))
    
    end_time = time.time()
    print(f"Multithreading ({num_threads} threads): {end_time - start_time:.2f} seconds")
    return len(results)

async def run_asyncio(num_tasks=4):
    start_time = time.time()
    numbers = list(range(35, 39))
    
    tasks = [async_heavy_computation(n) for n in numbers]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Asyncio ({num_tasks} tasks): {end_time - start_time:.2f} seconds")
    return len(results)

if __name__ == "__main__":
    print("Running benchmarks...\n")
    
    # Sequential
    seq_result = run_sequential()
    
    # Multiprocessing
    mp_result = run_multiprocessing()
    
    # Multithreading
    mt_result = run_multithreading()
    
    # Asyncio
    asyncio_result = asyncio.run(run_asyncio())
    
    print("\nVerification - All approaches completed same number of tasks:", 
          seq_result == mp_result == mt_result == asyncio_result)