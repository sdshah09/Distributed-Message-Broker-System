import socket
import time
import argparse

class Subscriber:
    def __init__(self, host='localhost', port=5555) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            self.client = None
    
    def subscribe(self, topic):
        if self.client:
            try:
                self._send_message(f"subscribe#{topic}")
                response = self._receive_message()
                print("Subscribed Response: ", response)
            except socket.error as e:
                print(f"Error during subscription: {e}")
    
    def listen_for_messages(self, topic):
        if self.client:
            print(f"Listening for new messages on topic '{topic}'...")
            try:
                while True:
                    self.pull(topic)
                    time.sleep(5)  # Sleep to simulate interval-based pulling
            except KeyboardInterrupt:
                print("\nSubscription stopped by user.")
                self.disconnect()
            except socket.error as e:
                print(f"Error while listening for messages: {e}")
    
    def pull(self, topic):
        if self.client:
            try:
                self._send_message(f"pull#{topic}")
                response = self._receive_message()
                if response:
                    print(f"New Message on '{topic}': {response}")
            except socket.error as e:
                print(f"Error pulling messages: {e}")
    
    def _send_message(self, message):
        try:
            self.client.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message: {e}")
        
    def _receive_message(self):
        try:
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            print(f"Error receiving message: {e}")
            return None

    def disconnect(self):
        if self.client:
            try:
                self.client.close()
                print("Client disconnected.")
            except socket.error as e:
                print(f"Error closing connection: {e}")

def main():
    parser = argparse.ArgumentParser(description="Subscriber for message broker")
    
    # Define command-line arguments
    parser.add_argument("--subscribe", type=str, help="Subscribe to the topic")
    
    args = parser.parse_args()
    print(args)
    # Initialize the publisher
    subscriber = Subscriber()

    # Handle --create flag to create a topic
    if args.subscribe:
        topic = args.subscribe
        print(f"Subscribin topic: {topic}")
        subscriber.subscribe(topic)

    subscriber.listen_for_messages(topic)
    # Close the connection
    subscriber.disconnect()

if __name__ == "__main__":
    main()
