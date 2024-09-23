import asyncio
import time

async def subscribe_benchmark(subscriber_id, topic, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)

    start_time = time.time()
    num_requests = 0
    
    # Run the benchmark for 5 seconds
    while time.time() - start_time < 5:
        # Send the subscribe request
        writer.write(f"subscribe#{topic}\n".encode('utf-8'))
        await writer.drain()

        # Read the response from the server
        response = await reader.read(1024)
        if b"successfully" in response:
            num_requests += 1
        
        # Introduce a short delay between subscriptions
        await asyncio.sleep(0.1)

    writer.close()
    await writer.wait_closed()

    end_time = time.time()
    throughput = num_requests / (end_time - start_time)
    print(f"Client {subscriber_id} subscribed {num_requests} times in 5 seconds. Throughput: {throughput:.2f} ops/sec")
    return throughput

async def benchmark_multiple_subscribers(num_clients, topic, host='localhost', port=5555):
    tasks = []
    for i in range(num_clients):
        subscriber_id = i + 1
        tasks.append(subscribe_benchmark(subscriber_id, f"{topic}_{subscriber_id}", host, port))

    throughputs = await asyncio.gather(*tasks)
    
    avg_throughput = sum(throughputs) / num_clients
    print(f"Average subscribe throughput with {num_clients} clients: {avg_throughput:.2f} ops/sec")

if __name__ == "__main__":
    topic = "benchmark_topic"  # Ensure the topic exists before running this
    num_clients = 10  # Adjust the number of clients
    asyncio.run(benchmark_multiple_subscribers(num_clients=num_clients, topic=topic))
