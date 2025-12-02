
- Start the server locally
uvicorn app.main:app --reload --port 8038

- Build image
docker build -t image-service .

- Start container based on above image
docker run --env-file .env_docker -p 8038:8000 image-service

- Build image and start container
docker compose up --build




