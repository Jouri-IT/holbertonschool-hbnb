# HBnB Evolution Phase 4: Simple Web Client — Sukoon

## Overview

This phase delivers the front-end of the HBnB Evolution project: a static web client that talks to the Flask REST API built in [Part 3](../part3/).

Instead of a generic listing UI, the client is themed as **Sukoon** — a fictional private desert resort in the AlUla highlands of Saudi Arabia. The site presents five luxury residences, lets visitors browse listings and details, and allows authenticated guests to submit reviews. All dynamic data (places, amenities, reviews, authentication) comes from the API; the client adds resort photography, typography, and editorial copy on top.

The stack is plain **HTML5**, **CSS3**, and **JavaScript (ES6)** with no frameworks. A single shared script (`scripts.js`) handles every page.

---

## What This Client Does

| Page | File | Purpose |
|------|------|---------|
| Residences (home) | `base_files/index.html` | Hero, philosophy section, and a grid of place cards loaded from the API |
| Login | `base_files/login.html` | Email/password sign-in; stores a JWT in a browser cookie |
| Place details | `base_files/place.html` | Full residence view: host, price, description, amenities, and reviews |
| Add review | `base_files/add_review.html` | Authenticated form to submit a star rating and written review |

### Key Behaviors

- **API-driven listings** — On load, the index page fetches all places from `GET /api/v1/places/` and rebuilds the card grid in JavaScript. Static placeholder cards in the HTML are replaced at runtime.
- **Price filtering** — A dropdown filters visible cards client-side by maximum nightly rate (no extra API call).
- **JWT session** — After login, the access token is saved in a `token` cookie (`SameSite=Lax`, 1-day expiry) and sent as `Authorization: Bearer …` on protected requests.
- **Conditional UI** — The header login link hides when a token exists. The “Add a Review” button on place details only appears for signed-in users. The review page redirects unauthenticated visitors back to the index.
- **Presentation layer** — The API returns title, description, price, coordinates, owner, amenities, and reviews — but not resort photos or card labels. A `PLACE_PRESENTATION` map in `scripts.js` pairs known residence titles with curated images and eyebrow text; unknown places still render with a neutral fallback.
- **CORS** — The Part 3 API enables `flask-cors` on `/api/v1/*` so the browser can call the API from a separate origin (e.g. a local static file server on port 5500 while Flask runs on port 5000).

---

## Architecture

```text
┌─────────────────────────┐         Fetch API          ┌──────────────────────────┐
│  Part 4 — Static Client │  ───────────────────────►  │  Part 3 — Flask REST API │
│  (HTML / CSS / JS)      │  ◄───────────────────────  │  (JWT, SQLAlchemy, SQLite)│
└─────────────────────────┘         JSON + JWT         └──────────────────────────┘
```

The client is fully decoupled from the backend: it only needs the API base URL (`http://127.0.0.1:5000/api/v1` in `scripts.js`) and can be served by any static file host.

---

## Repository Structure

```text
part4/
├── README.md                 # This file
├── base_files/               # Deliverable web client
│   ├── index.html            # Home — list of residences
│   ├── login.html            # Login form
│   ├── place.html            # Single residence + reviews
│   ├── add_review.html       # Submit a review (auth required)
│   ├── scripts.js            # Shared client logic (login, fetch, filter, review)
│   ├── styles.css            # Sukoon design system (Task 0)
│   └── images/               # Logo, amenity icons, resort photography
├── task_00_design.md         # Design task specification
├── task_01_login.md          # Login task specification
├── task_02_index.md          # Index / list task specification
├── task_03_place.md          # Place details task specification
├── task_04_add_review.md     # Add review task specification
└── manual_review/            # Peer evaluation checklist
```

---

## API Endpoints Used

| Method | Endpoint | Used on | Auth |
|--------|----------|---------|------|
| `POST` | `/api/v1/auth/login` | Login | No |
| `GET` | `/api/v1/places/` | Index | Optional |
| `GET` | `/api/v1/places/<id>` | Place details, Add review (title) | Optional |
| `POST` | `/api/v1/reviews/` | Add review | Required |

Request and response shapes match the Part 3 Swagger docs at `http://127.0.0.1:5000/api/v1/`.

---

## Design — Sukoon

Task 0 reskins the assignment template into a minimal luxury resort brand:

- **Palette** — Cream, sand, stone, and charcoal with a muted brass accent
- **Typography** — Cormorant Garamond (headings) and Jost (body), loaded from Google Fonts
- **Residences** — Five seeded places in Part 3 (Desert Pavilion, Garden Villa, Private Pool Villa, Mountain Suite, Royal Residence) each have matching photography under `images/resort/`
- **Accessibility** — Semantic HTML5 landmarks, screen-reader-only headings where needed, and meaningful `alt` text on images

Required assignment structure (header with logo/login button, footer, card dimensions, `#ddd` card borders, etc.) is preserved inside the custom theme.

---

## Installation and Running

You need **two processes**: the Part 3 API and a static server for the client.

### 1. Start the API (Part 3)

From the `part3/` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

The API listens at `http://127.0.0.1:5000`. On first run it seeds the Sukoon residences, amenities, sample reviews, and a default admin user.

### 2. Serve the client (Part 4)

From the `part4/base_files/` directory, use any static file server. Examples:

```bash
# Python
python3 -m http.server 5500

# Or VS Code / Cursor Live Server, etc.
```

Open `http://127.0.0.1:5500/index.html` (port may vary).

> **CORS:** If you see cross-origin errors in the browser console, confirm Part 3 is running and that `flask-cors` is enabled in `part3/app/__init__.py`. See [this article](https://medium.com/@mterrano1/cors-in-a-flask-api-38051388f8cc) for background on CORS in Flask.

### 3. Test credentials

Default admin (seeded at API startup):

| Field | Value |
|-------|-------|
| Email | `admin@hbnb.io` |
| Password | `admin1234` |

You can also register a new user through the Part 3 API (`POST /api/v1/users/`) and log in with that account.

---

## User Flows

### Browse residences (no login required)

1. Open `index.html`.
2. The client fetches places and renders cards with image, title, description, and price.
3. Use the **Nightly Rate** filter to show only residences within a budget.

### Log in

1. Open `login.html` and submit email + password.
2. On success, the JWT is stored in the `token` cookie and the browser redirects to `index.html`.
3. The header **Login** link is hidden while the cookie is present.

### View a residence

1. Click **View Details** on any card (links to `place.html?id=<place_id>`).
2. The client loads place data, owner, amenities (with icon mapping for WiFi, bed, bath/pool), and existing reviews.
3. If logged in, an **Add a Review** button links to the review form for that place.

### Submit a review (login required)

1. Open `add_review.html?id=<place_id>` (or follow the link from place details).
2. If there is no `token` cookie, the client redirects to `index.html`.
3. Fill in review text and rating, then submit.
4. On success, the form resets and a confirmation message is shown.

---

## Technologies

- HTML5 (semantic structure)
- CSS3 (custom properties, flexbox, responsive layout)
- JavaScript ES6 (`fetch`, `async`/`await`, DOM APIs, cookies)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- Part 3 backend: Flask, Flask-JWT-Extended, Flask-CORS, SQLAlchemy

---

## Task Mapping

| Assignment task | Implementation |
|-----------------|----------------|
| Task 1 — Design | `styles.css` + completed HTML for all four pages (Sukoon theme) |
| Task 2 — Login | `login.html` + `handleLoginSubmit()` / cookie helpers in `scripts.js` |
| Task 3 — List of places | `index.html` + `initIndexPage()`, `fetchPlaces()`, price filter |
| Task 4 — Place details | `place.html` + `initPlacePage()`, dynamic reviews and amenities |
| Task 5 — Add review | `add_review.html` + `initAddReviewPage()`, auth gate and `POST /reviews/` |

---

## Team Members

- Reema Almujalli
- Jouri AlSulaiman
- Razan Kashr

---

## Goal

Connect the HBnB REST API to a polished, interactive front-end: authenticate users with JWT cookies, load and display places and reviews without full page reloads, and demonstrate modern client-side patterns (Fetch, DOM rendering, form handling, and session-aware UI) in a cohesive branded experience.
