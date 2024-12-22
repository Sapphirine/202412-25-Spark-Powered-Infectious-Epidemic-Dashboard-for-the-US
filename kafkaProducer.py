from confluent_kafka import Producer
import csv


# Kafka producer config
conf = {
    'bootstrap.servers': 'localhost:9092'
}

# Kafka topic
topic = 'covid'

# initialize Kafka producer
producer = Producer(conf)


# Reading CSV files and sending data to Kafka
def send_to_kafka(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert each row of data to a string and send it to Kafka
            data = ','.join([f"{key}:{value}" for key, value in row.items()])
            producer.produce(topic, data)
            # Wait for the message to complete
            producer.poll(0)

    # Refresh producer
    producer.flush()


if __name__ == '__main__':
    csv_file_path = './data/test.csv'
    send_to_kafka(csv_file_path)


