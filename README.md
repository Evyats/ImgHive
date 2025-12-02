
## Overview
Local microservices stack for:
- FastAPI API (`image-service`)
- Celery worker
- Redis (task broker)
- MongoDB (metadata)
- Local file storage (`/s3`)

## Prerequisites
- Docker & Docker Compose
- Node.js (for frontend)
- Python 3.12 (optional local dev)

## First-time setup
Frontend deps:
`npm --prefix frontend install`

Storage folders:
`mkdir s3\image-storage s3\temp-storage`

## Start all services
MongoDB:
`docker compose -f backend\image-db\docker-compose.yml up`

Backend API:
`docker compose -f backend\image-service\docker-compose.yml up`

Upload pipeline (redis/producer/consumer):
`docker compose -f backend\image-upload\docker-compose.yml up`

Frontend:
`npm --prefix frontend run dev`

## Access
App URL: http://localhost:5173/

## Screenshots
<img src="frontend/src/assets/screenshots/Screenshot 2025-11-26 190734.png" width="320" alt="Landing" />
<img src="frontend/src/assets/screenshots/Screenshot 2025-11-26 190740.png" width="320" alt="Upload form" />
<img src="frontend/src/assets/screenshots/Screenshot 2025-11-26 190825.png" width="320" alt="Progress view" />
<img src="frontend/src/assets/screenshots/Screenshot 2025-11-27 180142.png" width="320" alt="Gallery grid" />
<img src="frontend/src/assets/screenshots/Screenshot 2025-11-27 180152.png" width="320" alt="Gallery detail" />
