import matplotlib.pyplot as plt

# Example data for createTopic, send, subscribe, and ping-pong tests
clients = [1, 3, 4, 10]  # Number of clients

# Throughput data from your tests (adjusted as per your logs)
create_topic_throughput = [4245.38, 4245.37, 4245.36]  # Throughput for createTopic (ops/sec)
send_throughput = [9.84, 9.82]  # Throughput for send (ops/sec)
subscribe_throughput = [0.20, 0.20, 0.08, 0.00] 
ping_pong_publisher_throughput = [1408.80, 1588.82, 948.98]  # Throughput for ping-pong test (messages/sec for publishers)
ping_pong_subscriber_throughput = [2274.20, 1288.22, 1539.48]  # Throughput for ping-pong test (messages/sec for subscribers)

# Plot createTopic throughput
plt.figure(figsize=(10, 6))
plt.plot(clients[:3], create_topic_throughput, label="Create Topic Throughput", marker='o')
plt.xlabel("Number of Clients")
plt.ylabel("Throughput (ops/sec)")
plt.title("Create Topic Throughput vs Number of Clients")
plt.grid(True)
plt.legend()
plt.show()

# Plot send throughput
plt.figure(figsize=(10, 6))
plt.plot(clients[:2], send_throughput, label="Send Message Throughput", marker='o', color='green')
plt.xlabel("Number of Clients")
plt.ylabel("Throughput (ops/sec)")
plt.title("Send Message Throughput vs Number of Clients")
plt.grid(True)
plt.legend()
plt.show()

# Plot subscribe throughput
plt.figure(figsize=(10, 6))
plt.plot(clients, subscribe_throughput, label="Subscribe Throughput", marker='o', color='red')
plt.xlabel("Number of Clients")
plt.ylabel("Throughput (ops/sec)")
plt.title("Subscribe Throughput vs Number of Clients")
plt.grid(True)
plt.legend()
plt.show()

# Plot ping-pong test throughput (publisher and subscriber)
plt.figure(figsize=(10, 6))
plt.plot(clients[:3], ping_pong_publisher_throughput, label="Ping-Pong Publisher Throughput", marker='o')
plt.plot(clients[:3], ping_pong_subscriber_throughput, label="Ping-Pong Subscriber Throughput", marker='o', color='purple')
plt.xlabel("Number of Clients")
plt.ylabel("Throughput (messages/sec)")
plt.title("Ping-Pong Test Throughput (Publisher & Subscriber) vs Number of Clients")
plt.grid(True)
plt.legend()
plt.show()
