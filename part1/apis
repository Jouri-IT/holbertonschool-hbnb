## API Interaction Flow

This section walks through four representative API calls and how a request moves through the system: client → Presentation Layer → `HBnBFacade` → Business Logic Layer → Persistence Layer, and back. The Presentation Layer only ever talks to the facade, as described in Section 2.

### User Registration

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

#### API Call Description

This API call creates a new user account by validating the submitted information, generating a unique identifier, storing the new user in the database, and returning a successful creation response. The purpose of this sequence diagram is to illustrate how the Presentation, Business Logic, and Persistence layers collaborate to process a user registration request while maintaining separation of concerns.

#### Flow of Interactions

1. The client sends a `POST /users` request to the Presentation Layer.
2. The Presentation Layer forwards the request to the `HBnBFacade`.
3. The facade invokes the `User` model to validate the data and create a new `User` object.
4. The `UserRepository` stores the new user in the database.
5. A confirmation is returned through the facade and Presentation Layer.
6. The client receives a **201 Created** response containing the new user information.

---

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

#### API Call Description

This API call creates a new place listing for an existing user. It validates the provided information, creates a `Place` object, stores it in the database, and returns the newly created resource. The purpose of this sequence diagram is to demonstrate how the application's layered architecture processes a place creation request from start to finish.

#### Flow of Interactions

1. The client sends a `POST /places` request.
2. The Presentation Layer forwards the request to the `HBnBFacade`.
3. The facade calls the `Place` model to validate the owner and create a new `Place` object.
4. The `PlaceRepository` persists the object in the database.
5. The repository returns a confirmation to the facade.
6. The Presentation Layer returns a **201 Created** response to the client.

---

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

#### API Call Description

This API call allows a user to submit a review for a specific place. Before storing the review, the system validates that both the user and the place exist. The purpose of this sequence diagram is to show how validation, business logic, and data persistence interact to process a review submission.

#### Flow of Interactions

1. The client submits a review through the API.
2. The Presentation Layer forwards the request to the `HBnBFacade`.
3. The facade delegates validation to the `Review` model.
4. After successful validation, the `ReviewRepository` stores the review.
5. The repository returns confirmation to the facade.
6. The client receives a **201 Created** response containing the newly created review.

---

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

#### API Call Description

This API call retrieves a list of places that match optional filtering criteria supplied by the client. The filters are validated before querying the database. The purpose of this sequence diagram is to illustrate the complete request-response flow through each architectural layer during a read operation.

#### Flow of Interactions

1. The client sends a `GET /places` request with optional filters.
2. The Presentation Layer forwards the request to the `HBnBFacade`.
3. The facade asks the `Place` model to validate the filtering parameters.
4. The `PlaceRepository` queries the database using the validated filters.
5. The matching place records are returned to the facade.
6. The Presentation Layer sends a **200 OK** response containing the list of places back to the client.
