import socket
import sys
import argparse

class Publisher:
    def __init__(self, host='localhost', port=5555) -> None:
        # Create a TCP socket for the publisher
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the message broker server
        self.client.connect((host, port))
        # Initialize the publisher ID
        self.publisherId = 0

    def registerPublisher(self):
        # Increment the publisher ID and return it
        self.publisherId += 1
        return self.publisherId

    def createTopic(self, PID, topic):
        # Send a message to create a new topic
        self._send_message(f"createTopic#{topic}")
        # Receive the response from the server
        response = self._receive_message()
        print("Create Response: ", response)

    def deleteTopic(self, PID, topic):
        # Send a message to delete a topic
        self._send_message(f"deleteTopic#{topic}")
        # Receive the response from the server
        response = self._receive_message()
        print("Delete Response: ", response)

    def send(self, PID, topic, message):
        # Send a message to publish to a topic
        self._send_message(f"send#{topic}#{message}")
        # Receive the response from the server
        response = self._receive_message()
        print("Send Response: ", response)

    def _send_message(self, message):
        # Send a message to the server
        self.client.send(message.encode('utf-8'))

    def _receive_message(self):
        # Receive a response message from the server
        return self.client.recv(1024).decode('utf-8')

    def disconnect(self):
        # Close the socket connection
        self.client.close()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Publisher for message broker")
    
    # Define command-line arguments
    parser.add_argument("--create", type=str, help="Create a new topic")
    parser.add_argument("--publish", nargs=2, metavar=('topic', 'message'), help="Publish a message to a topic")
    parser.add_argument("--delete", type=str, help="Delete the existing topic")

    # Parse the command-line arguments
    args = parser.parse_args()
    print(args)

    # Initialize the publisher
    publisher = Publisher()

    # Handle --create flag to create a topic
    if args.create:
        topic = args.create
        print(f"Creating topic: {topic}")
        publisher.createTopic(1, topic)

    # Handle --publish flag to send a message
    if args.publish:
        topic, message = args.publish
        print(f"Publishing message to topic {topic}: {message}")
        publisher.send(1, topic, message)
    
    if args.delete:
        topic = args.delete
        print(f"Deleting Topic: {topic}")
        publisher.deleteTopic(1,topic)
    # Close the connection
    # publisher.disconnect()

if __name__ == "__main__":
    main()