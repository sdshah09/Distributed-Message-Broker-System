import socket
import threading
from collections import defaultdict

class MessageBroker:
    def __init__(self) -> None:
        self.topics = defaultdict(list)  # Store messages per topic
        self.subscribers = defaultdict(list)  # Store subscribers (client_socket) per topic
        self.lock = threading.Lock()  # Ensure thread-safe access

    def handle_client(self, client_socket):
        def print_thread_id():
            thread_id = threading.get_ident()
            print(f"Thread ID: {thread_id}")
        print_thread_id()

        try:
            while True:
                try:
                    request = client_socket.recv(1024).decode('utf-8')
                    if not request:
                        break
                    command, topic, *message = request.split('#')
                    if command == 'createTopic':
                        self.create_topic(topic, client_socket)
                    elif command == 'deleteTopic':
                        self.delete_topic(topic, client_socket)
                    elif command == 'send':
                        self.send_message(topic, ''.join(message), client_socket)
                    elif command == 'subscribe':
                        self.subscribe(topic, client_socket)
                    elif command == 'pull':
                        self.pull_messages(topic, client_socket)
                except ConnectionResetError:
                    print("Connection reset by client.")
                    break
                except BrokenPipeError:
                    print("Broken pipe error. The client may have disconnected.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print(f"Closing connection with client: {client_socket.getpeername()}")
            client_socket.close()
        
    def create_topic(self, topic, client_socket):
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []
                client_socket.send("Topic created successfully.".encode('utf-8'))
            else:
                client_socket.send("Topic already exists.".encode('utf-8'))

    def delete_topic(self, topic, client_socket):
        with self.lock:
            if topic in self.topics:
                del self.topics[topic]
                del self.subscribers[topic]
                client_socket.send("Topic deleted successfully.".encode('utf-8'))
            else:
                client_socket.send("Topic does not exist.".encode('utf-8'))

    def send_message(self, topic, message, client_socket):
        with self.lock:
            if topic in self.topics:
                self.topics[topic].append(message)
                print(f"Message sent: {message} to topic {topic}")

                # Send message to all subscribers of the topic
                for subscriber_socket in self.subscribers[topic]:
                    try:
                        subscriber_socket.send(f"Message from {topic}: {message}".encode('utf-8'))
                    except (ConnectionResetError, BrokenPipeError):
                        print("A subscriber has disconnected.")
                
                client_socket.send(f"Message sent to topic {topic} successfully.".encode('utf-8'))
            else:
                client_socket.send(f"Topic {topic} does not exist.".encode('utf-8'))

    def subscribe(self, topic, client_socket):
        with self.lock:
            if topic not in self.topics:
                client_socket.send(f"Topic {topic} does not exist.".encode('utf-8'))
                return

            if client_socket not in self.subscribers[topic]:
                self.subscribers[topic].append(client_socket)
                client_socket.send(f"Subscribed to topic {topic} successfully.".encode('utf-8'))
            else:
                client_socket.send(f"Already subscribed to topic {topic}.".encode('utf-8'))

    def pull_messages(self, topic, client_socket):
        with self.lock:
            if topic in self.topics and client_socket in self.subscribers[topic]:
                messages = self.topics[topic]
                if messages:
                    for subscribers in self.subscribers[topic]:
                        for message in messages:
                            subscribers.send(f"Message from {topic}: {message}".encode('utf-8'))
                    self.topics[topic] = []  # Clear messages after pulling
                else:
                    client_socket.send("No new messages.".encode('utf-8'))
            else:
                client_socket.send("Topic does not exist or not subscribed.".encode('utf-8'))

    def start(self, host='localhost', port=5555):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"New connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    broker = MessageBroker()
    broker.start()
