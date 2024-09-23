import asyncio
from collections import defaultdict

class AsyncMessageBroker:
    def __init__(self) -> None:
        self.topics = defaultdict(list)  # Store messages per topic
        self.subscribers = defaultdict(list)  # Store subscribers (client_socket) per topic

    async def handle_client(self, reader, writer):
        client_address = writer.get_extra_info('peername')
        print(f"New client connected: {client_address}")

        try:
            while True:
                # Read data from the client
                try:
                    data = await reader.read(1024)
                    if not data:
                        break

                    # Decode and parse the client request
                    request = data.decode().strip()
                    command, topic, *message = request.split('#')
                    # print(request)
                    # Handle different commands based on the client request
                    if command == 'createTopic':
                        await self.create_topic(topic, writer)
                    elif command == 'deleteTopic':
                        await self.delete_topic(topic, writer)
                    elif command == 'send':
                        # print("In send")
                        # print(''.join(message))
                        await self.send_message(topic, ''.join(message), writer)
                    elif command == 'subscribe':
                        await self.subscribe(topic, writer)
                    elif command == 'pull':
                        await self.pull_messages(topic, writer)
                except ConnectionResetError:
                    print(f"Connection reset by peer: {client_address}")
                    break
                except Exception as e:
                    print(f"Error handling client {client_address}: {e}")
                    break

        except Exception as e:
            print(f"Unhandled exception for client {client_address}: {e}")
        finally:
            # Clean up the subscriber and close the connection when the client disconnects
            print(f"Client disconnected: {client_address}")
            await self.cleanup_subscriber(writer)
            try:
                writer.close()
                await writer.wait_closed()
            except ConnectionResetError:
                print(f"Connection already reset: {client_address}")

    async def create_topic(self, topic, writer):
            # Create a new topic if it doesn't exist
            if topic not in self.topics:
                self.topics[topic] = []
                await self.send_response(writer, "Topic created successfully.")
            else:
                await self.send_response(writer, "Topic already exists.")

    async def delete_topic(self, topic, writer):
        # Delete a topic if it exists
        if topic in self.topics:
            del self.topics[topic]
            del self.subscribers[topic]
            await self.send_response(writer, "Topic deleted successfully.")
        else:
            await self.send_response(writer, "Topic does not exist.")

    async def send_message(self, topic, message, writer):
        # Send a message to a topic
        if topic in self.topics:
            # print("Inside send message function: ",self.topics)
            self.topics[topic].append(message)
            print(f"Message sent: {message} to topic {topic}")

            # Broadcast the message to all subscribers of the topic
            for subscriber_writer in self.subscribers[topic]:
                try:
                    await self.send_response(subscriber_writer, f"Message from {topic}: {message}")
                except Exception:
                    print(f"Failed to send message to subscriber.")
            
            await self.send_response(writer, f"Message sent to topic {topic} successfully.")
        else:
            await self.send_response(writer, f"Topic {topic} does not exist.")

    async def subscribe(self, topic, writer):
        # Subscribe a client to a topic
        # print(self.topics)
        if topic not in self.topics:
            await self.send_response(writer, f"Topic {topic} does not exist.")
        else:
            if writer not in self.subscribers[topic]:
                self.subscribers[topic].append(writer)
                await self.send_response(writer, f"Subscribed to topic {topic} successfully.")
            else:
                await self.send_response(writer, f"Already subscribed to topic {topic}.")

    async def pull_messages(self, topic, writer):
        # Pull messages from a topic for a subscribed client
        if topic in self.topics and writer in self.subscribers[topic]:
            messages = self.topics[topic]
            if messages:
                for message in messages:
                    await self.send_response(writer, f"Message from {topic}: {message}")
                self.topics[topic] = []  # Clear messages after pulling
            # else:
                # await self.send_response(writer, "No new messages.")
        else:
            await self.send_response(writer, "Topic does not exist or not subscribed.")

    async def cleanup_subscriber(self, writer):
        # Remove a subscriber from all subscribed topics when the client disconnects
        for topic, subscribers in self.subscribers.items():
            if writer in subscribers:
                subscribers.remove(writer)
                print(f"Removed subscriber from topic: {topic}")

    async def send_response(self, writer, message):
        # Send a response message to the client
        writer.write((message + "\n").encode('utf-8'))
        await writer.drain()

    async def start_server(self, host='localhost', port=5555):
        # Start the server and listen for client connections
        server = await asyncio.start_server(self.handle_client, host, port)
        print(f"Server started on {host}:{port}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    broker = AsyncMessageBroker()
    asyncio.run(broker.start_server())