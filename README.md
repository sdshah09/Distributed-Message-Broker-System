# Distributed Message Broker System

This is a distributed message broker system that follows the Publisher-Subscriber design pattern. It is implemented in Python and consists of three main components:

1. Message Broker (server.py)
2. Publisher (publisher.py)
3. Subscriber (subscriber.py)

## Features

- Publishers can register themselves with the message broker and publish messages to specific topics.
- Subscribers can register themselves with the message broker and subscribe to specific topics of interest.
- The message broker handles the distribution of messages from publishers to subscribers based on their subscriptions.
- The system supports multiple publishers and subscribers, allowing for a distributed and scalable architecture.
- The message broker ensures that messages are delivered to all subscribers of a topic.
- Subscribers can pull new messages from the message broker for the topics they are subscribed to.

## Prerequisites

- Python 3.x
- Install required dependencies (if any, e.g., asyncio or other libraries).

## Getting Started

1. Clone the repository:


## Usage

### Publisher

Running the Message Broker (Server)
Start the message broker (server) by running the server.py file:
```bash
python3 server.py
```
This starts the message broker on localhost:5555 by default. The server will listen for connections from both publishers and subscribers.
You should see the following output, indicating the server is running:
```text
Server started on localhost:5555
```
### Running a Publisher
- Open a new terminal window.
- Run the publisher.py script:
```bash
python3 publisher.py --create my_topic
```
- This command creates a new topic named my_topic and registers the publisher.
- To publish a message to the my_topic topic:
```python
python3 publisher.py --publish my_topic "Hello, world!"
```

- You should see confirmation that the message was successfully sent.
Additional commands for the publisher include:
- Create a topic: ```python3 publisher.py --create my_topic```
- Send a message: ```python3 publisher.py --publish my_topic "Your message here"```
- Delete a topic: ```python3 publisher.py --delete my_topic```

- Register as a publisher using the `registerPublisher()` function.
- Create topics using the `createTopic(topic)` function.
- Publish messages to a topic using the `send(topic, message)` function.
- Delete topics using the `deleteTopic(topic)` function.

## Subscriber
  ### Open another new terminal window.
- Run the subscriber.py script to subscribe to a topic:
```bash
python3 subscriber.py --subscribe my_topic
```


- Register as a subscriber using the `registerSubscriber()` function.
- Subscribe to topics of interest using the `subscribe(topic)` function.
- Pull new messages from subscribed topics using the `pull(topic)` function.

    ### Configuration

- The message broker listens on `localhost` and port `5555` by default. You can modify these settings in the `server.py` file.

## Documentation

- Inline code comments are provided to explain the functionality of each component.


## Benchmarking
- To run performance benchmarks for the message broker, use the provided benchmarking scripts. For example:

- Run the createTopic benchmark:

```bash
python3 benchmark_createTopic.py
```
Run the send message benchmark:

```bash
python3 benchmark_send.py
```
- These scripts will simulate multiple clients and measure throughput for different operations. Detailed results will be printed to the console
## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).