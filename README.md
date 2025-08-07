# DocuManager

DocuManager is a Django-based document management system designed for organizing, categorizing, and extracting text from PDF documents. The project supports document categorization, participant management, and automated text extraction using Celery, RabbitMQ, and Redis.

---

## Features

- **Document Management**: Upload, categorize, and manage PDF documents.
- **Text Extraction**: Automatically extract text from uploaded PDFs using `pdftotext`.
- **Soft Deletion**: Support for soft deletion of categories, types, and documents.
- **Participant Management**: Manage participants and associate them with documents.
- **REST API**: Built with Django REST Framework and documented with Swagger (drf-spectacular).
- **Asynchronous Processing**: Uses Celery for background tasks like text extraction.
- **Dockerized**: Ready to run with Docker and Docker Compose for fast development and deployment.

---

## Project Structure

```
.
├── core/
│   ├── apps/
│   │   ├── documents/         # Document management app
│   │   └── participants/      # Participant management app
│   ├── config/                # Project settings and celery config
│   ├── manage.py
│   └── db.sqlite3
├── docker/                    # Docker-related files
├── envs/                      # Environment variable files
├── static/                    # Collected static files
├── media/                     # Uploaded media files
├── requirements.txt
├── docker-compose.yaml
├── LICENSE
└── README.md
```

---

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Environment Variables

Edit the files in the `envs/` directory as needed:

- `envs/web.env`: Django and Celery settings
- `envs/postgres.env`: PostgreSQL settings

### Run with Docker

```sh
docker-compose up --build
```

- Django app will be available at [http://localhost:8000](http://localhost:8000)
- Swagger API docs: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)

### Default Admin

The admin user is created automatically with the following credentials (can be changed in `envs/web.env`):

- Username: `django`
- Email: `django@gmail.com`
- Password: `1234`

---

## API

- **Admin Panel**: `/admin/`
- **Document Categories**: `/documents/categories/`
- **Documents**: `/documents/`
- **Swagger/OpenAPI Docs**: `/api/schema/swagger/`

---

## Main Components

### Documents App

- Models: DocumentCategory, DocumentType, Document, UploadedTextFile
- Text extraction: `extract_text_from_document` in `tasks/extract_text.py`
- Utilities: `extract_pdf_text` in `utils/document_helpers.py`

### Participants App

- Model: Participant

---



## License

This project is licensed under the [MIT License](LICENSE).

---

## Resources

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Redis](https://redis.io/)
- [pdftotext](https://github.com/jalan/pdftotext)