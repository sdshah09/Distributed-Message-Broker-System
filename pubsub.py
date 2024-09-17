# This is an event driven

class PubSub:
    def __init__(self) -> None:
        self.subscribers = {} # Stores topic and it's subscribers
        self.topics = [] # Stores topics and messages passed through the topics
        self.messages = {} # To store the messages for specific topics
        
    def createTopic(self,topic): # Create a topic to which publisher and subscriber can connect
        if topic not in self.topics:
            self.topics.append(topic)
            self.subscribers[topic] = []
            self.messages[topic] = []
            
    def deleteTopic(self,topic): # Deletes the whole topic and also every subscriber will be disconnected from this particular topic
        if topic in self.topics:
            self.topics.remove(topic)
            del self.subscribers[topic]
            del self.messages[topic]
            
    def send(self,topic,message):
        if topic in self.topics:
            self.messages[topic].append(message)
            
    def subscribe(self,topic):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(self)
            
    def unsubscribe(self,event,callback):
        if event in self.subscribers:
            self.subscribers[event].remove(callback)
            
    def publish(self,event,data):
        print("Subscribers when publish the data on specific topic",self.subscribers)
        if event in self.subscribers:
            for callback in self.subscribers[event]:
                callback(data)

def userAdded(user):
    print(f"User added: {user['name']}")
def userLocation(user):
    print(f"User Location: {user['location']}")
def userAge(age):
    print(f"User Age: {age}")

if __name__ == "__main__":
    pubsub = PubSub()
    pubsub.subscribe('userAdded', userAdded)
    pubsub.subscribe('userAdded', userLocation)
    pubsub.subscribe('userAge',userAge)
    pubsub.publish('userAdded',{'name':'Shaswat Shah','location':'Chicago'}) # If same topic and multiple callbacks we need to make sure data is in the same topic and is published once otherwise according to this architecture it will try to find the published message which does not exist
    # pubsub.publish('userAdded',{'location':'Chicago'})
    pubsub.publish('userAge',24)






























