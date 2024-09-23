import asyncio
import time

async def create_topic_benchmark(publisher_id, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)
    
    start_time = time.time()
    num_requests = 0
    
    while time.time() - start_time < 10:  # Run the benchmark for 60 seconds
        topic_name = f"benchmark_topic_{publisher_id}_{num_requests}"
        writer.write(f"createTopic#{topic_name}\n".encode('utf-8'))
        await writer.drain()

        response = await reader.read(1024)
        if b"successfully" in response:
            num_requests += 1
    
    writer.close()
    await writer.wait_closed()

    end_time = time.time()
    throughput = num_requests / (end_time - start_time)
    print(f"Client {publisher_id} created {num_requests} topics in 60 seconds. Throughput: {throughput:.2f} ops/sec")
    return throughput

async def benchmark_multiple_clients(num_clients, host='localhost', port=5555):
    tasks = []
    for i in range(num_clients):
        publisher_id = i + 1
        tasks.append(create_topic_benchmark(publisher_id, host, port))

    throughputs = await asyncio.gather(*tasks)
    
    avg_throughput = sum(throughputs) / num_clients
    print(f"Average throughput with {num_clients} clients: {avg_throughput:.2f} ops/sec")

if __name__ == "__main__":
    num_clients = 3  # You can increase this to test more clients
    asyncio.run(benchmark_multiple_clients(num_clients=num_clients))
