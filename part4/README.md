# HBnB - Simple Web Client

## Overview

Part 4 focuses on developing a simple web client for the HBnB application using HTML5, CSS3, and JavaScript ES6.

The client connects to the HBnB REST API developed in the previous phases and provides an interactive user interface for authentication, browsing places, viewing place details, and adding reviews.

## Objectives

- Develop a user-friendly web interface following the provided design.
- Implement client-side functionality using JavaScript ES6.
- Connect the web client to the HBnB REST API.
- Implement JWT authentication and session management.
- Store the JWT token in a cookie.
- Display and filter places.
- Display detailed place information.
- Allow authenticated users to add reviews.
- Use Fetch/AJAX to communicate with the backend API.
- Handle authentication and CORS.

## Technologies

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- REST API
- JWT Authentication
- Cookies

## Tasks

### Task 0 - Design

Complete the provided HTML and CSS files according to the design specifications.

Create the following pages:

- Login
- List of Places
- Place Details
- Add Review

### Task 1 - Login

Implement login functionality using the backend API.

The JWT token returned by the API is stored in a cookie for session management.

### Task 2 - List of Places

Implement the main page to:

- Display a list of all places.
- Fetch places from the API.
- Filter places on the client side based on country selection.
- Redirect unauthenticated users to the login page when required.

### Task 3 - Place Details

Implement the detailed view of a place.

The page should:

- Fetch place details using the place ID.
- Display the place information.
- Provide access to the Add Review form for authenticated users.

### Task 4 - Add Review

Implement a form to add a review for a place.

The form should only be accessible to authenticated users. Unauthenticated users should be redirected to the index page.

## Testing

The application should be tested to verify:

- Successful and failed login.
- JWT cookie creation.
- Places are retrieved from the API.
- Client-side filtering works correctly.
- Place details are displayed correctly.
- Authenticated users can access the review form.
- Unauthenticated users are redirected correctly.
- Reviews can be submitted successfully.
- API errors are handled correctly.

## Technologies

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- REST API
- JWT Authentication

## Team Members

- Razan Kashr
- Reema Almujalli
- Jouri AlSulaiman

## Goal

The goal of this phase is to build an interactive web client that connects the HBnB front-end with the existing REST API while providing authentication, place browsing, place details, and review functionality.
