import socket
import time
import argparse

class Subscriber:
    def __init__(self, host='localhost', port=5555) -> None:
        # Create a TCP socket for the subscriber
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the message broker server
            self.client.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            self.client = None
    
    def subscribe(self, topic):
        if self.client:
            try:
                # Send a message to subscribe to a topic
                self._send_message(f"subscribe#{topic}")
                # Receive the response from the server
                response = self._receive_message()
                print("Subscribed Response: ", response)
            except socket.error as e:
                print(f"Error during subscription: {e}")
    
    def listen_for_messages(self, topic):
        if self.client:
            print(f"Listening for new messages on topic '{topic}'...")
            try:
                while True:
                    # Pull messages from the subscribed topic
                    self.pull(topic)
                    # time.sleep(5)  # Sleep to simulate interval-based pulling
            except KeyboardInterrupt:
                print("\nSubscription stopped by user.")
                self.disconnect()
            except socket.error as e:
                print(f"Error while listening for messages: {e}")
    
    def pull(self, topic):
        if self.client:
            try:
                # Send a message to pull messages from a topic
                self._send_message(f"pull#{topic}")
                # Receive the response from the server
                response = self._receive_message()
                if response:
                    print(f"New Message on '{topic}': {response}")
            except socket.error as e:
                print(f"Error pulling messages: {e}")
    
    def _send_message(self, message):
        try:
            # Send a message to the server
            self.client.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message: {e}")
        
    def _receive_message(self):
        try:
            # Receive a response message from the server
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            print(f"Error receiving message: {e}")
            return None

    def disconnect(self):
        if self.client:
            try:
                # Close the socket connection
                self.client.close()
                print("Client disconnected.")
            except socket.error as e:
                print(f"Error closing connection: {e}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Subscriber for message broker")
    
    # Define command-line arguments
    parser.add_argument("--subscribe", type=str, help="Subscribe to the topic")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    print(args)

    # Initialize the subscriber
    subscriber = Subscriber()

    # Handle --subscribe flag to subscribe to a topic
    if args.subscribe:
        topic = args.subscribe
        print(f"Subscribing to topic: {topic}")
        subscriber.subscribe(topic)

    # Listen for messages on the subscribed topic
    subscriber.listen_for_messages(topic)

    # Close the connection
    subscriber.disconnect()

if __name__ == "__main__":
    main()