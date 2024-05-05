import os
import json
from confluent_kafka import Consumer
from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv


load_dotenv()

bootstrap_servers = os.getenv("KAFKA_SERVER")

producer_conf = {"bootstrap.servers": bootstrap_servers}

consumer_conf = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": os.getenv("GROUP_ID_FILTER"),
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_conf)
topic = "filnotification"
consumer.subscribe([topic])

email_sender = os.getenv("EMAIL_MAIN")
email_password = os.getenv("EMAIL_PASSWORD")


def email(msg):

    msg_json = json.loads(msg)
    subject = f"{msg_json['title']}"
    body = f"""
    
    {msg_json['title']}

    {msg_json['description']}

    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = {msg_json["emailReciever"]}
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, {msg_json["emailReciever"]}, em.as_string())


while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print("Received message: {}".format(msg.value().decode("utf-8")))
    email(msg.value().decode("utf-8"))
