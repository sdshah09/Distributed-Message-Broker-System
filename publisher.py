import socket

class Publisher:
    def __init__(self, host='localhost', port=5555) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def createTopic(self, topic):
        self._send_message(f"createTopic#{topic}")
        response = self._receive_message()
        print("Create Response: ", response)
        
    def deleteTopic(self, topic):
        self._send_message(f"deleteTopic#{topic}")
        response = self._receive_message()
        print("Delete Response: ", response)
        
    def send(self, topic, message):
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
    publisher = Publisher()
    
    while True:
        print("\nOptions:")
        print("1. Create Topic")
        print("2. Send Message")
        print("3. Delete Topic")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            topic = input("Enter topic name: ")
            publisher.createTopic(topic)
        elif choice == '2':
            topic = input("Enter topic name: ")
            message = input("Enter message: ")
            publisher.send(topic, message)
        elif choice == '3':
            topic = input("Enter topic name to delete: ")
            publisher.deleteTopic(topic)
        elif choice == '4':
            publisher.disconnect()
            print("Disconnected from server. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
