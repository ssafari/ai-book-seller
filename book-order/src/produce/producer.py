from confluent_kafka import Producer


class KafkaProducer():
    ''' Kafka broker configuration for local instance '''
    producer_config = {
        'bootstrap.servers': 'localhost:9092'  # Replace with your Kafka broker address if different
    }
    TOPIC = "book-order"

    def __init__(self):
        # Create a Producer instance
        self.producer = Producer(self.producer_config)

    # Define a callback for delivery reports (optional)
    def delivery_report(self, err, msg):
        ''' Callback function '''
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to topic '{msg.topic()}' partition [{msg.partition()}] @ offset {msg.offset()}")

    def send_book_order(self, msg: bytes):
        ''' Send message to Kafka '''
        self.producer.produce(self.TOPIC, value=msg, callback=self.delivery_report)
        # Wait for any outstanding messages to be delivered
        # and delivery report callbacks to be triggered
        self.producer.flush()
