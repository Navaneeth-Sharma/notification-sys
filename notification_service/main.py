import os
from fastapi import FastAPI
from pydantic import BaseModel
import json
from confluent_kafka import Producer
from dotenv import load_dotenv


load_dotenv()

class Notification(BaseModel):
    title: str
    description: str = ""
    tags: list = []
    userMail: str
    emailReciever: str


app = FastAPI()


consumer_conf = {
    "bootstrap.servers": os.getenv("KAFKA_SERVER"),
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}

producer = Producer(consumer_conf)


@app.post("/notify")
async def create_item(notification: Notification):
    producer.produce("notification", value=json.dumps(dict(notification)))
    return notification
