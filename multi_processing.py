from multiprocessing import Pool, Process, Queue, Lock, Pipe
import time
import os

def cpu_bound_task(n):
    return sum(i * i for i in range(n))

class MultiprocessingDemo:
    @staticmethod
    def basic_pool_test():
        numbers = [10**7 + x for x in range(4)]

        # Sequential execution
        start = time.time()
        result1 = list(cpu_bound_task(n) for n in numbers)
        print(f"Sequential execution time: {time.time() - start}")

        # Parallel execution with multiprocessing
        start = time.time()
        with Pool(processes=4) as pool:
            results2 = pool.map(cpu_bound_task, numbers)
        print(f"Parallel execution time: {time.time() - start}")

    def process_communication_via_queue():
        def worker(queue, lock):
            with lock:
                print(f"Worker {os.getpid()} started")
            result = cpu_bound_task(10**7)
            # put the result in the queue
            queue.put(result)
        queue = Queue()
        lock = Lock()
        processes = [Process(target=worker, args=(queue, lock)) for _ in range(4)]
        for p in processes:
            p.start()
        # get results from the queue
        results = [queue.get() for _ in processes]
        # wait for all processes to finish
        for p in processes:
            p.join()
        print(results)

    def producer_consumer_via_queue():
        def producer(queue):
            print(f"Producer {os.getpid()} started")
            for i in range(5):
                item = f"Item {i}"
                queue.put(item)
                print(f"Produced {item}")
                time.sleep(1)
        def consumer(queue):
            print(f"Consumer {os.getpid()} started")
            while True:
                item = queue.get()
                if item is None:
                    break
                print(f"Consumed {item}")
        queue = Queue()
        producer_process = Process(target=producer, args=(queue,))
        consumer_process = Process(target=consumer, args=(queue,))
        producer_process.start()
        consumer_process.start()
        producer_process.join()
        # add a None to the queue to signal the consumer to exit
        queue.put(None)
        consumer_process.join()

from multiprocessing import Value
class LockDemo:
    @staticmethod
    def counter_without_lock():
        counter = Value('i', 0)
        def increment_counter(counter: Value):
            print(f"Process {os.getpid()} started")
            counter.value += 1
            print(f"Process {os.getpid()} incremented counter to {counter.value}")
        processes = [Process(target=increment_counter, args=(counter,)) for _ in range(10000)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print(counter.value)

    @staticmethod
    def counter_with_lock():
        counter = Value('i', 0)
        lock = Lock()
        def increment_counter(counter: Value, lock: Lock):
            with lock:
                counter.value += 1
            print(f"Process {os.getpid()} incremented counter to {counter.value}")
        processes = [Process(target=increment_counter, args=(counter, lock)) for _ in range(10000)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print(counter.value)

class PipeDemo:
    @staticmethod
    def basic_pipe_communication():
        def sender(conn):
            print(f"Sender {os.getpid()} started")
            conn.send("Hello from the sender")
            conn.send([1, 2, 3, 4, 5])
            conn.send({"a": 1, "b": 2})
            conn.close()
            print(f"Sender {os.getpid()} finished")
        def receiver(conn):
            print(f"Receiver {os.getpid()} started")
            while True:
                try:
                    msg = conn.recv()
                    print(f"Received {msg}")
                except EOFError:
                    print("Receiver EOFError")
                    break
                except ConnectionError:
                    print("Receiver ConnectionError")
                    break
            print(f"Receiver {os.getpid()} finished")
        send_conn, recv_conn = Pipe()
        p1 = Process(target=sender, args=(send_conn,))
        p2 = Process(target=receiver, args=(recv_conn,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        # close the connection
        send_conn.close()
        recv_conn.close()


if __name__ == "__main__":
    # MultiprocessingDemo.basic_pool_test()
    # MultiprocessingDemo.process_communication_via_queue()
    # MultiprocessingDemo.producer_consumer_via_queue()

    # LockDemo.counter_without_lock()
    # LockDemo.counter_with_lock()
    PipeDemo.basic_pipe_communication()
