# Notification System



1. Add a `.env` file, take sample of .env.example to each service and change accordingly

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

