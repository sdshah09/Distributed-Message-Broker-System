import asyncio
import time

async def pull_message_benchmark(subscriber_id, topic, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)

    # First, subscribe to the topic to ensure we are subscribed before pulling
    writer.write(f"subscribe#{topic}\n".encode('utf-8'))
    await writer.drain()

    response = await reader.read(1024)  # Wait for subscription success
    if b"successfully" not in response:
        print(f"Client {subscriber_id} failed to subscribe to {topic}")
        return 0

    start_time = time.time()
    num_requests = 0

    # Run the benchmark for 5 seconds, pulling messages
    while time.time() - start_time < 5:
        writer.write(f"pull#{topic}\n".encode('utf-8'))
        await writer.drain()

        # Wait for the response from the server
        response = await reader.read(1024)
        if response:
            num_requests += 1

        # Introduce a short delay between pull requests
        await asyncio.sleep(0.1)

    writer.close()
    await writer.wait_closed()

    end_time = time.time()
    throughput = num_requests / (end_time - start_time)
    print(f"Client {subscriber_id} pulled {num_requests} messages in 5 seconds. Throughput: {throughput:.2f} ops/sec")
    return throughput

async def benchmark_multiple_pullers(num_clients, topic, host='localhost', port=5555):
    tasks = []
    for i in range(num_clients):
        subscriber_id = i + 1
        tasks.append(pull_message_benchmark(subscriber_id, f"{topic}_{subscriber_id}", host, port))

    throughputs = await asyncio.gather(*tasks)
    
    avg_throughput = sum(throughputs) / num_clients
    print(f"Average pull throughput with {num_clients} clients: {avg_throughput:.2f} ops/sec")

if __name__ == "__main__":
    topic = "benchmark_topic"  # Ensure the topic exists and has messages before running this
    num_clients = 3  # Adjust the number of clients
    asyncio.run(benchmark_multiple_pullers(num_clients=num_clients, topic=topic))
