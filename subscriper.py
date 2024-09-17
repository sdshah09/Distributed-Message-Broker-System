import socket

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
    
    def pull(self, topic):
        if self.client:
            try:
                self._send_message(f"pull#{topic}")
                response = self._receive_message()
                print("Pulled Response is: ", response)
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
            return "Error"

    def disconnect(self):
        if self.client:
            try:
                self.client.close()
                print("Client disconnected.")
            except socket.error as e:
                print(f"Error closing connection: {e}")

def main():
    subscriber1 = Subscriber()
    subscriber2 = Subscriber()
    subscriber3 = Subscriber()
    subscriber4 = Subscriber()
    subscriber5 = Subscriber()

    # Subscribe to topic
    subscriber1.subscribe("Shaswat")
    subscriber2.subscribe("Shaswat")
    subscriber3.subscribe("Shaswat")
    subscriber4.subscribe("Shaswat")
    subscriber5.subscribe("Shaswat")

    # Pull messages from topic
    subscriber1.pull("Shaswat")
    subscriber2.pull("Shaswat")
    subscriber3.pull("Shaswat")
    subscriber4.pull("Shaswat")
    subscriber5.pull("Shaswat")

    # Disconnect
    subscriber1.disconnect()
    subscriber2.disconnect()
    subscriber3.disconnect()
    subscriber4.disconnect()
    subscriber5.disconnect()

if __name__ == "__main__":
    main()
