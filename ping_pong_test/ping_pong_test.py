import asyncio
import time

# Shared synchronization event using asyncio
topic_ready_event = asyncio.Event()

# Publisher client
async def publisher_ping(publisher_id, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)
    
    topic = f"ping_topic_{publisher_id}"
    
    # Create the topic
    writer.write(f"createTopic#{topic}\n".encode('utf-8'))
    await writer.drain()
    
    response = await reader.read(1024)
    if "successfully" in response.decode('utf-8'):
        print(f"Publisher {publisher_id}: Topic {topic} created successfully.")
        topic_ready_event.set()  # Signal the subscriber that the topic is ready
    
    # Send 50 ping messages
    num_requests = 0
    start_time = time.time()

    for i in range(50):
        message = f"ping_message_{i}"
        writer.write(f"send#{topic}#{message}\n".encode('utf-8'))
        await writer.drain()
        await reader.read(1024)  # Acknowledge sending message
        num_requests += 1
        asyncio.wait(0.1)
    end_time = time.time()
    writer.close()
    await writer.wait_closed()

    # Measure throughput
    throughput = num_requests / (end_time - start_time)
    print(f"Publisher {publisher_id} throughput: {throughput:.2f} messages/sec")

# Subscriber client
async def subscriber_pong(subscriber_id, host='localhost', port=5555):
    reader, writer = await asyncio.open_connection(host, port)
    
    topic = f"ping_topic_{subscriber_id}"
    
    # Wait for the topic to be created
    await topic_ready_event.wait()
    
    # Subscribe to the topic
    writer.write(f"subscribe#{topic}\n".encode('utf-8'))
    await writer.drain()
    
    response = await reader.read(1024)
    if "successfully" in response.decode('utf-8'):
        print(f"Subscriber {subscriber_id}: Subscribed to topic {topic}.")
    
    # Pull 50 messages
    num_requests = 0
    start_time = time.time()

    for i in range(50):
        writer.write(f"pull#{topic}\n".encode('utf-8'))
        await writer.drain()
        response = await reader.read(1024)
        if response:
            print(f"Subscriber {subscriber_id} received: {response.decode('utf-8')}")
            num_requests += 1
        asyncio.wait(0.1)

    end_time = time.time()
    writer.close()
    await writer.wait_closed()

    # Measure throughput
    throughput = num_requests / (end_time - start_time)
    print(f"Subscriber {subscriber_id} throughput: {throughput:.2f} messages/sec")

# Test function to run publisher and subscriber
async def ping_pong_test(num_pairs, host='localhost', port=5555):
    tasks = []
    
    for i in range(num_pairs):
        pub_task = asyncio.create_task(publisher_ping(i + 1, host, port))
        sub_task = asyncio.create_task(subscriber_pong(i + 1, host, port))
        tasks.extend([pub_task, sub_task])
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    num_pairs = 4  # Set this to 2 for the two publisher-subscriber pairs
    asyncio.run(ping_pong_test(num_pairs=num_pairs))
