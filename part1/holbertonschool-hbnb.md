# HBnB Evolution — Part 1: Technical Documentation

**High-Level Architecture, Business Logic Design, and API Interaction Flows**

Repository: `holbertonschool-hbnb` — Directory: `part1`

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [High-Level Architecture](#2-high-level-architecture)
   - [2.1 The Three Layers](#21-the-three-layers)
   - [2.2 The Facade Pattern](#22-the-facade-pattern)
   - [2.3 Package Diagram](#23-package-diagram)
3. [Business Logic Layer](#3-business-logic-layer)
   - [3.1 Class Diagram](#31-class-diagram)
   - [3.2 Entity Descriptions](#32-entity-descriptions)
   - [3.3 Relationships](#33-relationships)
4. [API Interaction Flow](#4-api-interaction-flow)
   - [4.1 User Registration](#41-user-registration)
   - [4.2 Place Creation](#42-place-creation)
   - [4.3 Review Submission](#43-review-submission)
   - [4.4 Fetching a List of Places](#44-fetching-a-list-of-places)
5. [Conclusion](#5-conclusion)

---

## 1. Introduction

This is the technical design for Part 1 of HBnB Evolution — a simplified AirBnB-style platform. Users can register, list properties ("places"), leave reviews on places they've stayed at, and attach amenities to listings.

The goal here is to lay out the architecture before any code gets written, so Parts 2 (API) and 3 (persistence) build on a design that's already been thought through rather than improvised along the way.

The system is covered from three angles:

- a package diagram showing the layered architecture
- a class diagram for the domain model (Business Logic layer)
- sequence diagrams walking through the main API calls

The first two describe what the system looks like; the third describes how it actually behaves at runtime. Between them you get a full picture of the structure and the flow of data through it.

---

## 2. High-Level Architecture

HBnB Evolution follows a three-layer architecture. Splitting things this way keeps each layer focused on one job and means a change in, say, the database doesn't ripple up into the business rules or the API.

### 2.1 The Three Layers

**Presentation Layer**
This is the entry point — the API endpoints clients hit to register users, manage places, submit reviews, and manage amenities. It handles incoming requests, does basic formatting/validation, and hands everything off to the Business Logic Layer. No business rules live here, and it never talks to the database directly.

**Business Logic Layer**
This is where the actual domain lives: `User`, `Place`, `Review`, and `Amenity`, plus the rules that govern them — validation, relationships, anything that needs to stay consistent. It also handles operations that touch more than one entity, like checking that a review's place and user both actually exist before creating it.

**Persistence Layer**
Handles storing and retrieving data. It's organized as one repository per entity, each translating domain operations into database calls (create, read, update, delete). The actual database tech isn't decided yet — that comes in Part 3 — so for now this layer is kept generic.

### 2.2 The Facade Pattern

The Presentation Layer never talks to the Business Logic Layer directly — everything goes through a single facade, `HBnBFacade`. It exposes one method per operation (`register_user()`, `create_place()`, `submit_review()`, `list_places()`, etc.), so the API doesn't need to know anything about how those operations are actually implemented underneath.

A few reasons this is worth doing:

- **Decoupling** — the API only depends on the facade's interface, not on the internals of the Business Logic Layer, so either side can change without breaking the other.
- **Simpler endpoints** — a multi-step operation (validate owner → create place → persist → confirm) collapses into a single call from the API's point of view.
- **Clear responsibilities** — the facade orchestrates, the models enforce the rules, the repositories handle storage. Nobody's job overlaps.

The Business Logic Layer then talks to the Persistence Layer on its own to actually read or write data.

### 2.3 Package Diagram

```mermaid
classDiagram
    class PresentationLayer {
        <<Layer>>
        +UserAPI
        +PlaceAPI
        +ReviewAPI
        +AmenityAPI
    }

    class HBnBFacade {
        <<Facade>>
        +register_user()
        +update_user()
        +create_place()
        +update_place()
        +list_places()
        +submit_review()
        +update_review()
        +delete_review()
        +list_reviews_by_place()
        +create_amenity()
        +update_amenity()
        +delete_amenity()
        +list_amenities()
    }

    class BusinessLogicLayer {
        <<Layer>>
        +User
        +Place
        +Review
        +Amenity
    }

    class PersistenceLayer {
        <<Layer>>
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
    }

    PresentationLayer ..> HBnBFacade : uses (Facade Pattern)
    HBnBFacade ..> BusinessLogicLayer : delegates business operations
    BusinessLogicLayer ..> PersistenceLayer : performs CRUD operations
```

**Figure 1 — High-level package diagram** showing the Presentation, Business Logic, and Persistence layers, communicating through the `HBnBFacade`.

The `PresentationLayer` package groups the API endpoints (`UserAPI`, `PlaceAPI`, `ReviewAPI`, `AmenityAPI`). Every call from here goes through `HBnBFacade`, which then delegates to `BusinessLogicLayer` — the four domain models. That layer talks to `PersistenceLayer`, where each entity has its own repository. Notice the Presentation Layer never has a direct line to the Persistence Layer; everything routes through the Business Logic Layer in between.

---

## 3. Business Logic Layer

This layer is built around four entities: **User**, **Place**, **Review**, and **Amenity**. Each one gets a UUID4 `id`, plus `created_at` and `updated_at` timestamps — that part's the same across the board, for auditing.

### 3.1 Class Diagram

```mermaid
classDiagram
    class User {
        +UUID id
        -String first_name
        -String last_name
        -String email
        -String password
        -Boolean is_admin
        -DateTime created_at
        -DateTime updated_at
        +register()
        +update_profile(data)
        +delete()
    }

    class Place {
        +UUID id
        -String title
        -String description
        -Float price
        -Float latitude
        -Float longitude
        -DateTime created_at
        -DateTime updated_at
        +create()
        +update(data)
        +delete()
        +list()
        +add_amenity(amenity)
        +remove_amenity(amenity)
    }

    class Review {
        +UUID id
        -Integer rating
        -String comment
        -DateTime created_at
        -DateTime updated_at
        +create()
        +update(data)
        +delete()
        +list_by_place(place_id)
    }

    class Amenity {
        +UUID id
        -String name
        -String description
        -DateTime created_at
        -DateTime updated_at
        +create()
        +update(data)
        +delete()
        +list()
    }

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : receives
    Place "0..*" -- "0..*" Amenity : has
```

**Figure 2 — Detailed class diagram** for the Business Logic layer: User, Place, Review, and Amenity, with their attributes, methods, and relationships.

### 3.2 Entity Descriptions

**User**
A registered account on the platform — first name, last name, email, password, plus an `is_admin` flag to tell regular users apart from admins. Users can register, update their own profile, and be deleted. One user can own several places and write several reviews.

**Place**
A property listing created by a user — title, description, price, latitude, longitude. Every place has exactly one owner. Places support the usual create/update/delete/list operations, can have any number of amenities attached, and can receive any number of reviews.

**Review**
Feedback a user leaves on a place they've stayed at — a rating and a comment. Every review points to exactly one place and one user. Reviews can be created, updated, deleted, and listed per place.

**Amenity**
A feature a place can offer — Wi-Fi, parking, a pool, whatever. Just a name and a description. Amenities exist independently of any specific place and support their own create/update/delete/list operations.

### 3.3 Relationships

| Relationship | Multiplicity | Type | Description |
|---|---|---|---|
| User → Place | 1 to 0..* | Association | A User owns zero or more Places; each Place has exactly one owner. |
| User → Review | 1 to 0..* | Association | A User writes zero or more Reviews; each Review has exactly one author. |
| Place → Review | 1 to 0..* | Association | A Place receives zero or more Reviews; each Review refers to exactly one Place. |
| Place ↔ Amenity | 0..* to 0..* | Association | A Place can have many Amenities, and an Amenity can be associated with many Places. |

All four entities also carry the same base fields — a UUID4 `id` and `created_at` / `updated_at` timestamps — so every record can be uniquely identified and traced over time.

---

## 4. API Interaction Flow

This section walks through four representative API calls and how a request moves through the system: client → Presentation Layer → `HBnBFacade` → Business Logic Layer → Persistence Layer, and back. The Presentation Layer only ever talks to the facade, same as described in Section 2.

### 4.1 User Registration

The client sends new user details to the API. The facade hands the data to the `User` model to validate and instantiate; once a `User` object exists with a fresh UUID, the facade tells `UserRepository` to save it. Confirmation flows back up through the facade and API to the client.

```mermaid
sequenceDiagram
    actor Client
    participant API as PresentationLayer (API)
    participant Facade as HBnBFacade
    participant UserModel as User (BusinessLogic)
    participant Repo as UserRepository (Persistence)

    Client->>API: POST /users (first_name, last_name, email, password)
    API->>Facade: register_user(data)
    Facade->>UserModel: validate and instantiate User
    UserModel-->>Facade: User object (with new UUID)
    Facade->>Repo: save(user)
    Repo->>Repo: INSERT INTO users
    Repo-->>Facade: confirmation (user_id)
    Facade-->>API: user created (201)
    API-->>Client: 201 Created (user data)
```

**Figure 3 — Sequence diagram for the User Registration API call.**

### 4.2 Place Creation

The client sends place details, including who owns it. The facade passes this to the `Place` model, which validates and creates a new `Place` object. The facade saves it via `PlaceRepository` and sends a confirmation back.

```mermaid
sequenceDiagram
    actor Client
    participant API as PresentationLayer (API)
    participant Facade as HBnBFacade
    participant PlaceModel as Place (BusinessLogic)
    participant Repo as PlaceRepository (Persistence)

    Client->>API: POST /places (title, description, price, latitude, longitude, owner_id)
    API->>Facade: create_place(data)
    Facade->>PlaceModel: validate owner and instantiate Place
    PlaceModel-->>Facade: Place object (with new UUID)
    Facade->>Repo: save(place)
    Repo->>Repo: INSERT INTO places
    Repo-->>Facade: confirmation (place_id)
    Facade-->>API: place created (201)
    API-->>Client: 201 Created (place data)
```

**Figure 4 — Sequence diagram for the Place Creation API call.**

### 4.3 Review Submission

The client sends a rating and comment for a place. The facade passes this to the `Review` model, which checks that the place and user both exist before creating the `Review` object. The facade saves it through `ReviewRepository` and confirms back to the client.

```mermaid
sequenceDiagram
    actor Client
    participant API as PresentationLayer (API)
    participant Facade as HBnBFacade
    participant ReviewModel as Review (BusinessLogic)
    participant Repo as ReviewRepository (Persistence)

    Client->>API: POST /places/{place_id}/reviews (rating, comment, user_id)
    API->>Facade: submit_review(place_id, data)
    Facade->>ReviewModel: validate place and user, instantiate Review
    ReviewModel-->>Facade: Review object (with new UUID)
    Facade->>Repo: save(review)
    Repo->>Repo: INSERT INTO reviews
    Repo-->>Facade: confirmation (review_id)
    Facade-->>API: review created (201)
    API-->>Client: 201 Created (review data)
```

**Figure 5 — Sequence diagram for the Review Submission API call.**

### 4.4 Fetching a List of Places

The client requests places, optionally with filters (price range, location, etc.). The facade passes the filters to the `Place` model to apply any business rules, then queries `PlaceRepository`. The resulting list flows back through the facade, the API, and finally to the client.

```mermaid
sequenceDiagram
    actor Client
    participant API as PresentationLayer (API)
    participant Facade as HBnBFacade
    participant PlaceModel as Place (BusinessLogic)
    participant Repo as PlaceRepository (Persistence)

    Client->>API: GET /places?filters
    API->>Facade: list_places(filters)
    Facade->>PlaceModel: apply business rules to filters
    PlaceModel-->>Facade: validated query parameters
    Facade->>Repo: find(filters)
    Repo->>Repo: SELECT * FROM places WHERE ...
    Repo-->>Facade: list of place records
    Facade-->>API: list of Place objects
    API-->>Client: 200 OK (places data)
```

**Figure 6 — Sequence diagram for the Fetching a List of Places API call.**

---

## 5. Conclusion

That covers the design for Part 1: a package diagram for the three-layer architecture and how the facade ties them together, a class diagram for the Business Logic entities and how they relate, and four sequence diagrams tracing real API calls end-to-end through all three layers.

This should be enough to start building from in Part 2 (the API itself) and Part 3 (hooking up a real database), without having to make architectural decisions on the fly.
