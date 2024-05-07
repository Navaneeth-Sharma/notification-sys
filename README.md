# Notification System

## System Design

![image](https://github.com/Navaneeth-Sharma/notification-sys/assets/63489382/52076dcf-8af7-4a9c-913b-d29f8e536fbf)

Features active
- [x] Restrict user level requests to send notification
- [x] Email 
- [ ] SMS
- [ ] Custom App handler
- [ ] Analytics

### Tech Stack Used 
- Confluent Kafka to setup Server and module
- Redis to store and count the number of requests each day
- FastAPI
- SMTP
- Docker to containerize it and make each thing a different service


## How to run this locally

1. Add `.env` files for each service and take .env.example for reference and change accordingly

2. Run Docker Compose to start local the kafka and redis servers and 3 different services
```docker-compose up```

3. send a post request to `localhost:3000` with body
    ```json
        {
            "title": "thenav",
            "description": "Awesome !!This is a cool notification",
            "tags": ["hiTag"],
            "userMail": "mainuser@email.com",
            "emailReciever": "youwanttosend@email.com"
        }
    ```

The max count is 10 per day for each `title` for now.

