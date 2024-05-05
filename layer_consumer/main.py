import os
from confluent_kafka import Consumer
import redis
import json
from confluent_kafka import Producer, Consumer
from dotenv import load_dotenv


load_dotenv()

bootstrap_servers = os.getenv("KAFKA_SERVER")

consumer_conf = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": os.getenv("GROUP_ID_BASE"),
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_conf)
topic = "notification"
consumer.subscribe([topic])

r = redis.Redis(host="redis", port=6379, decode_responses=True)


producer_conf = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": os.getenv("GROUP_ID_FILTER"),
    "auto.offset.reset": "earliest",
}

producer = Producer(producer_conf)


def push_event(msg):
    producer.produce("filnotification", value=msg)


MAX_REQUESTS = 10


def validator(msg):
    msg_json = json.loads(msg)
    if r.get(msg_json["title"]):
        cnt = int(r.get(msg_json["title"])) + 1
        ttl = r.ttl(msg_json["title"])
        r.set(msg_json["title"], str(cnt))
        if ttl > 0:
            r.expire(msg_json["title"], ttl)
    else:
        r.set(msg_json["title"], 1)
        r.expire(msg_json["title"], 86400)

    if r.get(msg_json["title"]) and int(r.get(msg_json["title"])) > MAX_REQUESTS:
        print("maxed out the requests")

        return
    else:
        push_event(msg)


while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    validator(msg.value().decode("utf-8"))
    print("Received message: {}".format(msg.value().decode("utf-8")))
