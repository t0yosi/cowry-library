# Library Management System

## Architecture

- The Backend API uses Django Rest Framework with a PostgreSQL database to store admin data and user information.
- The Frontend API is built with FastAPI and uses MongoDB to store book data for quick access by users.
- RabbitMQ is used to communicate changes (like adding or removing books) between the two services.
- Docker is used to containerize and orchestrate the services.

## Technologies Used

- **Backend:** Django, Django REST Framework, PostgreSQL
- **Frontend:** FastAPI, Pydantic, MongoDB
- **Messaging Queue:** RabbitMQ
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest, Django's TestCase, REST framework test client, RabbitMQ
- **Other Tools:** HTTPX (for testing FastAPI routes)

## Features

### Backend/Admin API

- Add new books to the library catalog.
- Remove books from the catalog.
- Fetch list of users and their borrowing history.
- Fetch list of books that are currently borrowed and unavailable for lending.

### Frontend API

- Enroll users in the library system.
- Browse and filter books by publisher and category.
- Borrow books by specifying how many days you want them.
- Get book details by its ID.

## Project Structure

```bash
.
├── backend      # Django app for the backend/admin API
├── frontend_api       # FastAPI app for the frontend API
├── docker-compose.yml # Docker Compose file to orchestrate services
└── README.md          # Project README file
