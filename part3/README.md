# HBnB Evolution Phase 3: Authentication and Database Integration

## Overview

This phase extends the HBnB Evolution project by introducing secure authentication, authorization, and persistent database integration.

The project transitions from the in-memory repository implemented in Phase 2 to a database-backed architecture using SQLAlchemy and SQLite for development while preparing the application for MySQL in production.

The layered architecture established in previous phases is maintained, with communication between all layers handled through the **HBnBFacade**.

---

## Project Scope

This phase implements the following features:

- JWT Authentication
- Password Hashing using Bcrypt
- Role-Based Authorization
- SQLAlchemy ORM
- SQLite Database
- MySQL Configuration
- Persistent Repository Layer
- Entity Relationships
- Database Validation
- REST API Endpoints
- ER Diagram

---

## Architecture

The application follows a layered architecture:

- **Presentation Layer** – Flask REST API endpoints responsible for handling HTTP requests and responses.
- **Business Logic Layer** – Implements application rules and coordinates operations through the HBnBFacade.
- **Persistence Layer** – Uses SQLAlchemy repositories to interact with the database.
- **Database Layer** – Stores application data using SQLite during development and MySQL for production deployment.

---

## Technologies

- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- SQLAlchemy
- SQLite
- MySQL
- Flask-Bcrypt
- REST API

---

## Repository Structure

```
part3/
│
├── README.md
├── requirements.txt
├── config.py
├── run.py
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   ├── models/
│   ├── persistence/
│   └── services/
│
└── tests/
```

---

## Project Structure Description

### README.md
Contains the project overview, architecture, installation instructions, and documentation.

### requirements.txt
Lists all Python packages required to install and run the application.

### config.py
Stores application configuration including database settings, JWT configuration, and environment-specific options.

### run.py
Application entry point that creates and starts the Flask application.

### app/

Contains the main application source code.

#### app/__init__.py

Initializes the Flask application, loads configuration, registers API namespaces, and initializes extensions such as JWT and Bcrypt.

#### app/api/

Contains all REST API endpoints exposed to clients.

#### app/models/

Contains the business entities including User, Place, Review, and Amenity with their validation logic and SQLAlchemy mappings.

#### app/services/

Contains the **HBnBFacade**, which implements the business logic and coordinates communication between the API and persistence layers.

#### app/persistence/

Contains the repository implementations responsible for database operations using SQLAlchemy.

### tests/

Contains API and business logic tests used to validate the application's behavior.

---

## Installation

(Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python3 run.py
```

Open Swagger documentation

```
http://127.0.0.1:5000/api/v1/
```

---

## Deliverables

This phase delivers:

- JWT Authentication
- Password Hashing
- Authorization
- SQLAlchemy Integration
- SQLite Development Database
- MySQL Configuration
- Entity Relationship Mapping
- Repository Pattern Implementation
- Database Validation
- REST API
- ER Diagram
- Technical Documentation

---

## Team Members

- Razan Kashr
- Reema Almujalli
- Jouri AlSulaiman

---

## Goal

The objective of this phase is to transform the HBnB application into a secure, database-backed REST API by implementing authentication, authorization, persistent storage, and relational database management while preserving the layered architecture developed throughout the previous phases.
