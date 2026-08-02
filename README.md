# HBnB Evolution Phase 2: Business Logic and API Implementation

## Overview

This phase focuses on implementing the HBnB Evolution application based on the architecture designed in Phase 1.

The project establishes the application structure using a layered architecture and begins the implementation of the Business Logic, Presentation, and Persistence layers. It also introduces the Facade pattern to simplify communication between the different layers while keeping the code modular and maintainable.

## Project Scope

The implementation includes the core components of the application:

- User Management
- Place Management
- Review Management
- Amenity Management

The project is organized into the following layers:

- Presentation Layer (Flask REST API)
- Business Logic Layer
- Persistence Layer (In-Memory Repository)

Communication between these layers is managed through the **HBnBFacade**.

## Deliverables

This project includes:

- Project Structure Initialization
- Flask Application Setup
- Facade Pattern Implementation
- In-Memory Repository
- Business Logic Models
- REST API Endpoints
- Technical Documentation

## Technologies

- Python 3
- Flask
- Flask-RESTx
- REST API
- In-Memory Repository
- Facade Design Pattern

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── config.py
├── run.py
└── app/
    ├── __init__.py
    ├── api/
    │   └── v1/
    ├── models/
    ├── services/
    └── persistence/
```

## Installation and Running the Application

1. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python run.py
   ```

4. The API and its interactive Swagger documentation will be available at:

   ```text
   http://127.0.0.1:5000/api/v1/
   ```

## Team Members

- Reema Almujalli
- Jouri AlSulaiman
- Razan Kashr

## Goal

The goal of this phase is to transform the system design into a functional application by implementing the project structure, business logic, REST API foundation, and persistence layer, providing the foundation for future database integration and advanced application features.
