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

```

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+

### Steps to Set Up the Project

1. **Clone the repository:**

   ```bash
   git clone https://github.com/t0yosi/cowry-library.git
   cd cowry-library

   ```

2. **Create a .env file in the project root with the following content:**

   #### Backend Admin API (Django)

   ```bash
      POSTGRES_DB=library_db
      POSTGRES_USER=postgres
      POSTGRES_PASSWORD=password
      POSTGRES_HOST=db
   ```

   #### Frontend API (FastAPI)

   ```bash
      MONGODB_URL=mongodb://mongo:27017
   ```

3. **Start the docker container**

   
   ```bash
      docker-compose up --build
   ```

4. **Access the services:**   
   
   ```bash
      Frontend API (FastAPI): http://localhost:8000
      Backend API (Django): http://localhost:8001/api
   ```

## API Endpoints

### Frontend API Endpoints

**Base URL:** `http://localhost:8000`

| Method | Endpoint            | Description                            | Parameters                         |
| ------ | ------------------- | -------------------------------------- | ---------------------------------- |
| `POST` | `/users/`           | Enroll a new user                      | `email`, `first_name`, `last_name` |
| `GET`  | `/books/`           | List all available books               | None                               |
| `GET`  | `/books/{book_id}`  | Get details of a single book by its ID | `book_id`                          |
| `POST` | `/borrow/{book_id}` | Borrow a book                          | `book_id`, `days`                  |
| `GET`  | `/books/filter/`    | Filter books by publisher or category  | `publisher`, `category`            |

**Payloads:**
```bash
   ## Enroll a user:
   curl -X POST "http://localhost:8080/api/enroll_user/" -H "Content-Type: application/json" -d '{"email": "test@example.com", "firstname": "John", "lastname": "Doe"}'

   ## Get list of all books:
   curl -X POST "http://127.0.0.1:8000/books/{book_id}" 

   ## Fetch by Publisher:
   curl -X GET "http://127.0.0.1:8000/books/filter/?publisher=Ada%20Bane"

   ## Fetch by Category:
   curl -X GET "http://127.0.0.1:8000/books/filter/?category=Fiction"
   
   ## Borrow a book::
   curl -X POST "http://127.0.0.1:8000/books/{book_id}/borrow" -H "Content-Type: application/json" -d '{"days": 14}'
```

### Backend/Admin API Endpoints

**Base URL:** `http://localhost:8001`

| Method   | Endpoint               | Description                             | Parameters                       |
| -------- | ---------------------- | --------------------------------------- | -------------------------------- |
| `POST`   | `/api/books/`          | Add a new book to the catalog           | `title`, `publisher`, `category` |
| `GET   ` | `/api/books/{book_id}` | Add a book to the catalog               | `book_id`                        |
| `DELETE` | `/api/books/{book_id}` | Remove a book from the catalog          | `book_id`                        |
| `GET`    | `/api/users/`          | List all enrolled users                 | None                             |
| `GET`    | `/api/borrowed/`       | List all users and their borrowed books | None                             |

## Testing

### Unit Tests

Unit tests cover the core logic of the models, API endpoints, and services.

#### Backend API

Run unit tests for the Django backend:

```bash
docker-compose exec backend-api python manage.py test
```

#### Frontend API

Run unit tests for the FastAPI frontend-api:

```bash
docker-compose exec frontend-api pytest
```
