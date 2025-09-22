# Django Chatbot

A Django-based chatbot application. This project provides a foundation for building conversational AI using Django, with easy deployment via Docker.

## Features

- Django web framework
- Modular chatbot logic
- REST API endpoints
- Easy local development and Docker deployment

## Requirements

- Python 3.8+
- pip
- Docker (optional, for containerized deployment)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/srikanth-ahana/django_chatbot.git
cd django_chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to access the chatbot.

## Docker

### Build and run with Docker

1. **Build the Docker image:**

    ```bash
    docker build -t django_chatbot .
    ```

2. **Run the container:**

    ```bash
    docker run -d -p 8000:8000 django_chatbot
    ```

3. The chatbot will be available at [http://localhost:8000](http://localhost:8000).

### Example `Dockerfile`

```dockerfile
# Use official Python image
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Project Structure

```
django_chatbot/
├── manage.py
├── chatbot/           # Django app for chatbot logic
├── requirements.txt
├── Dockerfile
└── ...
```

## Customization

- Add your chatbot logic in the `chatbot` app.
- Update `requirements.txt` for additional dependencies.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

