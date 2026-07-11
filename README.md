# HBnB Evolution

A simplified AirBnB-like web application built as part of the Holberton School curriculum. This repository contains the documentation and implementation work for the HBnB project across multiple parts, including architectural planning, API development, and business logic modeling.

## Project Overview

HBnB Evolution allows users to:

- register and manage accounts;
- create and browse places;
- attach amenities to places;
- leave reviews for places;
- interact with a RESTful API built with Flask.

The project is organized into three main parts:

- Part 1: technical documentation and UML diagrams;
- Part 2: Flask application structure, business logic, and API endpoints;
- Part 3: database persistence and advanced backend integration.

## Tech Stack

- Python 3
- Flask
- Flask-RESTx
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-SQLAlchemy

## Repository Structure

```text
holbertonschool-hbnb/
├── part1/                  # Architecture diagrams and documentation
├── part2/
│   └── hbnb-part2/        # Flask API implementation and tests
└── part3/                  # Planned persistence/database work
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd holbertonschool-hbnb
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r part2/hbnb-part2/requirements.txt
```

### 4. Run the application

```bash
cd part2/hbnb-part2
python run.py
```

The API will be available at:

- http://127.0.0.1:5000
- Swagger documentation: http://127.0.0.1:5000/api/v1/

## Testing

The project includes model and API tests under the Part 2 implementation folder.

To run the available tests:

```bash
cd part2/hbnb-part2
python test_models.py
```

## Notes

This repository is currently focused on building a modular and scalable backend foundation for an AirBnB-inspired application. The design emphasizes a layered architecture, clear separation of concerns, and future expansion toward database-backed persistence.

## Author

Ian Aviles