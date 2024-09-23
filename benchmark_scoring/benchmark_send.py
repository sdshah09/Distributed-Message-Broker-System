import asyncio
import time

async def send_message_benchmark(publisher_id, topic, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)

    # Create the topic (only needs to be done once)
    writer.write(f"createTopic#{topic}\n".encode('utf-8'))
    await writer.drain()  # Ensure the message is sent
    await reader.read(1024)  # Wait for the response (assuming it’s "successfully")

    start_time = time.time()
    num_requests = 0
    
    # Send messages for 5 seconds
    while time.time() - start_time < 5:
        message = f"message_{publisher_id}_{num_requests}"
        writer.write(f"send#{topic}#{message}\n".encode('utf-8'))  # Ensure proper formatting
        await writer.drain()  # Flush the buffer to send the message

        response = await reader.read(1024)  # Read server response
        if b"successfully" in response:
            num_requests += 1
        
        # Introduce a short delay between sends
        await asyncio.sleep(0.1)

    writer.close()
    await writer.wait_closed()

    end_time = time.time()
    throughput = num_requests / (end_time - start_time)
    print(f"Client {publisher_id} sent {num_requests} messages in 5 seconds. Throughput: {throughput:.2f} ops/sec")
    return throughput

async def benchmark_multiple_senders(num_clients, topic, host='localhost', port=5555):
    
    tasks = []
    for i in range(num_clients):
        publisher_id = i + 1
        tasks.append(send_message_benchmark(publisher_id, f"{topic}_{publisher_id}", host, port))

    throughputs = await asyncio.gather(*tasks)
    
    avg_throughput = sum(throughputs) / num_clients
    print(f"Average send throughput with {num_clients} clients: {avg_throughput:.2f} ops/sec")

if __name__ == "__main__":
    topic = "benchmark_topic"  # Set the base topic name
    num_clients = 4  # Adjust the number of clients
    asyncio.run(benchmark_multiple_senders(num_clients=num_clients, topic=topic))
