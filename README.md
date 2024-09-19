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
- The message broker performs garbage collection of message buffers when all subscribers have read the messages.

## Prerequisites

- Python 3.x

## Getting Started

1. Clone the repository:


## Usage

### Publisher

- Register as a publisher using the `registerPublisher()` function.
- Create topics using the `createTopic(topic)` function.
- Publish messages to a topic using the `send(topic, message)` function.
- Delete topics using the `deleteTopic(topic)` function.

### Subscriber

- Register as a subscriber using the `registerSubscriber()` function.
- Subscribe to topics of interest using the `subscribe(topic)` function.
- Pull new messages from subscribed topics using the `pull(topic)` function.

## Configuration

- The message broker listens on `localhost` and port `5555` by default. You can modify these settings in the `server.py` file.

## Documentation

- Inline code comments are provided to explain the functionality of each component.
- API manual pages and detailed documentation can be found in the `docs` directory.

## Evaluation and Benchmarking

- The system includes evaluation scenarios and benchmarking tests to measure server throughput and performance under different conditions.
- Benchmark results and system design discussions can be found in the `reports` directory.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).