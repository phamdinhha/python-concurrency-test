import asyncio
import time

async def write(msg):
    print(f"Message writien: ", msg)

async def say1():
    await asyncio.sleep(2)
    await write("Hello")

async def say2():
    await asyncio.sleep(2)
    await write("World")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(asyncio.gather(
        say1(), say2()
    ))
    end = time.time()
    print("All tasks done")
    print(f"Execution time: {end - start}")
    loop.close()