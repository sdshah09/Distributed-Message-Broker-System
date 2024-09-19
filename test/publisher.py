import socket
import sys
import argparse

class Publisher:
    def __init__(self, host='localhost', port=5555) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.publisherId = 0

    def registerPublisher(self):
        self.publisherId += 1
        return self.publisherId

    def createTopic(self, PID,topic):
        self._send_message(f"createTopic#{topic}")
        response = self._receive_message()
        print("Create Response: ", response)

    def deleteTopic(self, PID, topic):
        self._send_message(f"deleteTopic#{topic}")
        response = self._receive_message()
        print("Delete Response: ", response)

    def send(self, PID, topic, message):
        self._send_message(f"send#{topic}#{message}")
        response = self._receive_message()
        print("Send Response: ", response)

    def _send_message(self, message):
        self.client.send(message.encode('utf-8'))

    def _receive_message(self):
        return self.client.recv(1024).decode('utf-8')

    def disconnect(self):
        self.client.close()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Publisher for message broker")
    
    # Define command-line arguments
    parser.add_argument("--create", type=str, help="Create a new topic")
    parser.add_argument("--publish", nargs=2, metavar=('topic', 'message'), help="Publish a message to a topic")
    
    args = parser.parse_args()
    print(args)
    # Initialize the publisher
    publisher = Publisher()

    # Handle --create flag to create a topic
    if args.create:
        topic = args.create
        print(f"Creating topic: {topic}")
        publisher.createTopic(1,topic)

    # Handle --publish flag to send a message
    if args.publish:
        topic, message = args.publish
        print(f"Publishing message to topic {topic}: {message}")
        publisher.send(1,topic, message)

    # Close the connection
    # publisher.disconnect()

if __name__ == "__main__":
    main()
