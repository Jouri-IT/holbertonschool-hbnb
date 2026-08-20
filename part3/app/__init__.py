from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.services import facade


def seed_admin(app):
    """Ensure a default admin user exists.

    is_admin is never settable through the public API, so without
    this there would be no way to ever obtain an admin JWT to test
    (or use) the admin-only endpoints. Runs once at startup; on
    later startups the email lookup below finds the row already
    committed from a previous run and returns early.
    """
    email = app.config["ADMIN_EMAIL"]
    if facade.get_user_by_email(email):
        return

    facade.create_user(
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": email,
            "password": app.config["ADMIN_PASSWORD"],
        },
        is_admin=True,
    )


SUKOON_AMENITIES = [
    "WiFi",
    "King Bed",
    "Air Conditioning",
    "Outdoor Rain Shower",
    "Private Terrace",
    "Garden Shower",
    "Private Courtyard",
    "Private Pool",
    "Sun Terrace",
    "Panoramic Terrace",
    "Fireplace",
    "Private Majlis Lounge",
    "Dedicated Butler",
]

SUKOON_RESIDENCES = [
    {
        "title": "Desert Pavilion",
        "description": (
            "Set low against a dune, the Desert Pavilion opens onto its own "
            "private terrace where sand meets a poured-concrete threshold."
        ),
        "price": 980,
        "latitude": 26.6084,
        "longitude": 37.9247,
        "amenities": [
            "WiFi", "King Bed", "Air Conditioning",
            "Outdoor Rain Shower", "Private Terrace",
        ],
    },
    {
        "title": "Garden Villa",
        "description": (
            "A private courtyard villa among stone pines, shaped by shadow "
            "and still air."
        ),
        "price": 860,
        "latitude": 26.6091,
        "longitude": 37.9231,
        "amenities": [
            "WiFi", "King Bed", "Air Conditioning",
            "Garden Shower", "Private Courtyard",
        ],
    },
    {
        "title": "Private Pool Villa",
        "description": (
            "An infinity edge that dissolves into the horizon, with a sun "
            "terrace built for slow mornings."
        ),
        "price": 1450,
        "latitude": 26.6078,
        "longitude": 37.9259,
        "amenities": [
            "WiFi", "King Bed", "Air Conditioning",
            "Private Pool", "Sun Terrace",
        ],
    },
    {
        "title": "Mountain Suite",
        "description": (
            "Perched above the highlands, facing dusk over stone, with a "
            "panoramic terrace for stargazing."
        ),
        "price": 1120,
        "latitude": 26.6102,
        "longitude": 37.9214,
        "amenities": [
            "WiFi", "King Bed", "Air Conditioning",
            "Panoramic Terrace", "Fireplace",
        ],
    },
    {
        "title": "Royal Residence",
        "description": (
            "The resort's signature address -- arched interiors, a private "
            "majlis lounge, and a dedicated estate host."
        ),
        "price": 2600,
        "latitude": 26.6069,
        "longitude": 37.9268,
        "amenities": [
            "WiFi", "King Bed", "Air Conditioning",
            "Private Majlis Lounge", "Dedicated Butler",
        ],
    },
]

# (guest email, first name, last name) -- seeded purely so reviews
# below have a real author to attach to; password is unused by
# anyone (these accounts aren't meant to be logged into).
SUKOON_GUESTS = {
    "elena": ("elena.marchetti@example.com", "Elena", "Marchetti"),
    "thomas": ("thomas.berg@example.com", "Thomas", "Berg"),
    "noura": ("noura.alzahrani@example.com", "Noura", "Al-Zahrani"),
    "james": ("james.whitfield@example.com", "James", "Whitfield"),
}

SUKOON_REVIEWS = [
    ("Desert Pavilion", "elena", 5,
     "Four nights, and I still think about the quiet each morning at the "
     "terrace. This is what rest actually feels like."),
    ("Desert Pavilion", "thomas", 4,
     "Beautifully understated design. The only thing I would change is "
     "staying longer."),
    ("Private Pool Villa", "noura", 5,
     "The infinity edge is not a metaphor. Best two nights of the year."),
    ("Royal Residence", "james", 5,
     "Impeccable. The majlis lounge alone justifies the stay."),
]


def seed_places(app):
    """Ensure the Sukoon showcase residences (with amenities) exist.

    Mirrors seed_admin(): without seed data the Part 4 client has
    nothing to fetch and render on a fresh database. Idempotent --
    skipped once any place already exists, so it never duplicates
    rows or clobbers edits made through the API.
    """
    if facade.get_all_places():
        return

    owner = facade.get_user_by_email(app.config["ADMIN_EMAIL"])
    if not owner:
        return

    amenity_ids = {}
    for name in SUKOON_AMENITIES:
        amenity = facade.create_amenity({"name": name})
        amenity_ids[name] = amenity.id

    for residence in SUKOON_RESIDENCES:
        data = {**residence, "owner_id": owner.id}
        data["amenities"] = [amenity_ids[name] for name in data["amenities"]]
        facade.create_place(data)


def seed_reviews(app):
    """Ensure a handful of sample guest reviews exist.

    Skipped once any review already exists. Guest accounts are
    created (idempotently, by email) purely to have a real author to
    attach each seeded review to.
    """
    if facade.get_all_reviews():
        return

    guest_ids = {}
    for key, (email, first_name, last_name) in SUKOON_GUESTS.items():
        guest = facade.get_user_by_email(email)
        if not guest:
            guest = facade.create_user({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": "guest-review-1234",
            })
        guest_ids[key] = guest.id

    places_by_title = {p.title: p for p in facade.get_all_places()}

    for title, guest_key, rating, text in SUKOON_REVIEWS:
        place = places_by_title.get(title)
        if not place:
            continue
        facade.create_review({
            "place_id": place.id,
            "user_id": guest_ids[guest_key],
            "rating": rating,
            "text": text,
        })


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Use Flask SECRET_KEY for JWT
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Allow the static Part 4 web client (served from a different
    # origin/port) to call this API from the browser.
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    with app.app_context():
        db.create_all()
        seed_admin(app)
        seed_places(app)
        seed_reviews(app)

    return app
