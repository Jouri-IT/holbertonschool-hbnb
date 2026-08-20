/*
  Sukoon — client-side scripts
  Part 4 / Task 1: Login
  Part 4 / Task 2: Index (list of places)
  Part 4 / Task 3: Place details
  Part 4 / Task 4: Add review

  Talks to the HBnB REST API (Part 3) to authenticate a user, list
  the resort's residences, show a single residence's details, submit
  a guest review, and keep a JWT cookie for later requests.
*/

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    updateLoginLinkVisibility();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await handleLoginSubmit(loginForm);
        });
    }

    // Each page below only wires up if its own markup is present, so
    // this one file stays safe to include, unmodified, on every page.
    if (document.getElementById('places-list')) {
        initIndexPage();
    }

    if (document.getElementById('place-details')) {
        initPlacePage();
    }

    if (document.getElementById('review-form')) {
        initAddReviewPage();
    }
});

/** Shows/hides the header's #login-link based on whether a JWT cookie exists. */
function updateLoginLinkVisibility() {
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = getCookie('token') ? 'none' : 'block';
    }
}

/* ---------- Login (Task 1) ---------- */

/**
 * Reads the form fields, calls the login endpoint, and reacts to
 * the result: store the token and redirect on success, show an
 * error message on failure.
 */
async function handleLoginSubmit(form) {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorBox = document.getElementById('login-error');
    const submitButton = form.querySelector('button[type="submit"]');

    hideMessage(errorBox);
    setButtonLoading(submitButton, true, 'Login');

    try {
        const response = await loginUser(email, password);

        if (response.ok) {
            const data = await response.json();
            setCookie('token', data.access_token, 1);
            window.location.href = 'index.html';
            return;
        }

        showMessage(errorBox, await extractErrorMessage(
            response,
            response.status === 401 ? 'Invalid email or password.' : 'Login failed. Please try again.'
        ));
    } catch (error) {
        showMessage(errorBox, 'Unable to reach the server. Please try again.');
    } finally {
        setButtonLoading(submitButton, false, 'Login');
    }
}

/** POSTs credentials to the login endpoint and returns the raw response. */
async function loginUser(email, password) {
    return fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
}

/** Pulls a readable error message out of a failed API response. */
async function extractErrorMessage(response, fallback) {
    try {
        const data = await response.json();
        if (data && (data.error || data.message)) {
            return data.error || data.message;
        }
    } catch (error) {
        // response body wasn't JSON — fall through to the default below
    }

    return fallback || 'Something went wrong. Please try again.';
}

/* ---------- Index page: list of places (Task 2) ---------- */

// The API only knows title/description/price/lat/long -- it has no
// concept of resort photography or card copy. This maps the five
// seeded Sukoon residences to the art direction from the Task 0
// design; any place the API returns that isn't in this map (e.g. one
// created later through the API) still renders correctly, just with
// a neutral fallback image and eyebrow instead of bespoke copy.
const PLACE_PRESENTATION = {
    'Desert Pavilion': { image: 'images/resort/desert-pavilion.jpg', eyebrow: '01 — Pavilion' },
    'Garden Villa': { image: 'images/resort/garden-villa.jpg', eyebrow: '02 — Villa' },
    'Private Pool Villa': { image: 'images/resort/pool-villa.jpg', eyebrow: '03 — Pool Villa' },
    'Mountain Suite': { image: 'images/resort/mountain-suite.jpg', eyebrow: '04 — Suite' },
    'Royal Residence': { image: 'images/resort/royal-residence.jpg', eyebrow: '05 — Residence' },
};
const DEFAULT_PLACE_PRESENTATION = { image: 'images/resort/hero.jpg', eyebrow: 'Residence' };

function initIndexPage() {
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener('change', handlePriceFilterChange);
    }

    fetchPlaces(getCookie('token'));
}

/** Fetches the list of places, attaching the JWT if one is available. */
async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    const headers = {};

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places/`, { headers });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        if (placesList) {
            placesList.innerHTML = '';
            placesList.appendChild(
                buildMessage('error-message', 'Unable to load residences right now. Please try again shortly.')
            );
        }
    }
}

/** Clears #places-list and renders one .place-card per place. */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (!places.length) {
        placesList.appendChild(buildMessage('place-tagline', 'No residences are available yet.'));
        return;
    }

    places.forEach((place) => {
        placesList.appendChild(buildPlaceCard(place));
    });
}

/** Builds a single .place-card element for a place returned by the API. */
function buildPlaceCard(place) {
    const presentation = PLACE_PRESENTATION[place.title] || DEFAULT_PLACE_PRESENTATION;

    const card = document.createElement('article');
    card.className = 'place-card';
    card.dataset.price = place.price;

    card.innerHTML = `
        <div class="place-card-image">
            <img src="${presentation.image}" alt="${escapeHtml(place.title)}">
        </div>
        <div class="place-card-body">
            <span class="eyebrow">${escapeHtml(presentation.eyebrow)}</span>
            <h2>${escapeHtml(place.title)}</h2>
            <p class="place-tagline">${escapeHtml(place.description || '')}</p>
            <p class="place-price">Price per night: <strong>$${formatPrice(place.price)}</strong></p>
            <a href="place.html?id=${encodeURIComponent(place.id)}" class="details-button">View Details</a>
        </div>
    `;

    return card;
}

/** Shows/hides rendered place cards based on the selected max price. */
function handlePriceFilterChange(event) {
    const maxPrice = event.target.value;
    const cards = document.querySelectorAll('#places-list .place-card');

    cards.forEach((card) => {
        const price = parseFloat(card.dataset.price);
        const withinBudget = maxPrice === 'all' || price <= parseFloat(maxPrice);
        card.style.display = withinBudget ? '' : 'none';
    });
}

/* ---------- Place details page (Task 3) ---------- */

function initPlacePage() {
    const token = getCookie('token');

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        showPlaceNotFound('No residence was specified.');
        return;
    }

    fetchPlaceDetails(token, placeId);
}

/** Extracts the ?id= query parameter from the current URL. */
function getPlaceIdFromURL() {
    return new URLSearchParams(window.location.search).get('id');
}

/** Fetches a single place's full details, attaching the JWT if available. */
async function fetchPlaceDetails(token, placeId) {
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places/${encodeURIComponent(placeId)}`, { headers });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        showPlaceNotFound("We couldn't find that residence. It may have been removed.");
    }
}

/** Populates the hero, #place-details and #reviews sections for one place. */
function displayPlaceDetails(place) {
    document.title = `${place.title} — Sukoon`;

    const presentation = PLACE_PRESENTATION[place.title] || DEFAULT_PLACE_PRESENTATION;

    const nameEl = document.getElementById('place-name');
    if (nameEl) nameEl.textContent = place.title;

    const heroImage = document.querySelector('.place-hero-image');
    if (heroImage) {
        heroImage.src = presentation.image;
        heroImage.alt = place.title;
    }

    const heroEyebrow = document.querySelector('.place-hero-content .eyebrow');
    if (heroEyebrow) heroEyebrow.textContent = presentation.eyebrow;

    renderPlaceInfo(place);
    renderReviews(place.reviews || []);

    const addReviewLink = document.querySelector('#add-review a.details-button');
    if (addReviewLink) {
        addReviewLink.setAttribute('href', `add_review.html?id=${encodeURIComponent(place.id)}`);
    }
}

/** Clears and rebuilds the host/price/description/amenities block. */
function renderPlaceInfo(place) {
    const detailsSection = document.getElementById('place-details');
    if (!detailsSection) return;

    const hostName = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Sukoon';

    const amenities = place.amenities || [];
    const amenitiesHtml = amenities.length
        ? amenities.map((a) => amenityListItem(a.name)).join('')
        : '<li>No amenities listed.</li>';

    const info = document.createElement('div');
    info.className = 'place-info';
    info.innerHTML = `
        <p><span class="field-label">Host</span><span id="place-host">${escapeHtml(hostName)}, Estate Host</span></p>
        <p><span class="field-label">Price per night</span>$<span id="place-price">${formatPrice(place.price)}</span></p>
        <p class="place-description" id="place-description">${escapeHtml(place.description || '')}</p>
        <div>
            <span class="field-label">Amenities</span>
            <ul class="amenities-list" id="place-amenities">${amenitiesHtml}</ul>
        </div>
    `;

    detailsSection.innerHTML = '<h2 class="sr-only">Residence Information</h2>';
    detailsSection.appendChild(info);
}

/** Maps an amenity name to one of the three provided icon images, if any. */
function amenityIconFor(name) {
    const key = name.toLowerCase();
    if (key.includes('wifi')) return 'images/icon_wifi.png';
    if (key.includes('bed')) return 'images/icon_bed.png';
    if (key.includes('shower') || key.includes('bath') || key.includes('pool')) return 'images/icon_bath.png';
    return null;
}

function amenityListItem(name) {
    const icon = amenityIconFor(name);
    const iconHtml = icon ? `<img src="${icon}" alt="" class="amenity-icon">` : '';
    return `<li>${iconHtml}${escapeHtml(name)}</li>`;
}

/** Clears and rebuilds the #reviews section from a list of review objects. */
function renderReviews(reviews) {
    const reviewsList = document.getElementById('reviews');
    if (!reviewsList) return;

    reviewsList.innerHTML = '';

    if (!reviews.length) {
        reviewsList.appendChild(
            buildMessage('place-tagline', 'No reviews yet — be the first to share your stay.')
        );
        return;
    }

    reviews.forEach((review) => {
        reviewsList.appendChild(buildReviewCard(review));
    });
}

function buildReviewCard(review) {
    const card = document.createElement('article');
    card.className = 'review-card';

    const authorName = review.user
        ? `${review.user.first_name} ${review.user.last_name}`
        : 'Guest';

    card.innerHTML = `
        <div class="review-card-body">
            <h3 class="review-author">${escapeHtml(authorName)}</h3>
            <p class="review-comment">${escapeHtml(review.text)}</p>
            <p class="review-rating">Rating: ${renderStars(review.rating)}</p>
        </div>
    `;

    return card;
}

function renderStars(rating) {
    const filled = Math.max(0, Math.min(5, Number(rating) || 0));
    return '★'.repeat(filled) + '☆'.repeat(5 - filled);
}

/** Replaces #place-details with an error message and hides reviews/add-review. */
function showPlaceNotFound(message) {
    const detailsSection = document.getElementById('place-details');
    if (detailsSection) {
        detailsSection.innerHTML = '';
        detailsSection.appendChild(buildMessage('error-message', message));
    }

    const reviewsList = document.getElementById('reviews');
    if (reviewsList) reviewsList.innerHTML = '';

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) addReviewSection.style.display = 'none';
}

/* ---------- Add review page (Task 4) ---------- */

function initAddReviewPage() {
    const token = getCookie('token');

    // Only authenticated users may reach this page at all.
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');

    if (!placeId) {
        if (reviewForm) reviewForm.hidden = true;
        showMessage(
            setMessageVariant(document.getElementById('review-message'), 'error-message'),
            'No residence was specified for this review.'
        );
        return;
    }

    loadReviewPlaceName(token, placeId);

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await handleReviewSubmit(reviewForm, token, placeId);
        });
    }
}

/** Fills in the "Reviewing: <name>" heading with the real place title. */
async function loadReviewPlaceName(token, placeId) {
    const nameEl = document.getElementById('review-place-name');
    if (!nameEl) return;

    try {
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await fetch(`${API_BASE_URL}/places/${encodeURIComponent(placeId)}`, { headers });
        if (!response.ok) return;

        const place = await response.json();
        nameEl.textContent = place.title;
        document.title = `Reviewing: ${place.title} — Sukoon`;
    } catch (error) {
        // Leave the default placeholder text in place -- this is a
        // cosmetic nicety, not something worth blocking the form for.
    }
}

/**
 * Reads the form fields, submits the review, and reacts to the
 * result: show a success message and clear the form, or show an
 * error message, leaving what the guest typed intact.
 */
async function handleReviewSubmit(form, token, placeId) {
    const reviewText = document.getElementById('review').value.trim();
    const rating = document.getElementById('rating').value;
    const messageBox = document.getElementById('review-message');
    const submitButton = form.querySelector('button[type="submit"]');

    hideMessage(messageBox);
    setButtonLoading(submitButton, true, 'Submit Review');

    try {
        const response = await submitReview(token, placeId, reviewText, rating);

        if (response.ok) {
            form.reset();
            setMessageVariant(messageBox, 'success-message');
            showMessage(messageBox, 'Thank you — your review has been submitted.');
        } else {
            setMessageVariant(messageBox, 'error-message');
            showMessage(messageBox, await extractErrorMessage(response, 'Failed to submit your review. Please try again.'));
        }
    } catch (error) {
        setMessageVariant(messageBox, 'error-message');
        showMessage(messageBox, 'Unable to reach the server. Please try again.');
    } finally {
        setButtonLoading(submitButton, false, 'Submit Review');
    }
}

/** POSTs a new review to the API and returns the raw response. */
async function submitReview(token, placeId, reviewText, rating) {
    return fetch(`${API_BASE_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: Number(rating),
            place_id: Number(placeId)
        })
    });
}

/* ---------- Shared helpers ---------- */

function buildMessage(className, text) {
    const el = document.createElement('p');
    el.className = className;
    el.textContent = text;
    return el;
}

function showMessage(el, message) {
    if (!el) return;
    el.textContent = message;
    el.hidden = false;
}

function hideMessage(el) {
    if (!el) return;
    el.hidden = true;
    el.textContent = '';
}

/** Swaps a message box between its error/success visual styles. */
function setMessageVariant(el, variant) {
    if (!el) return el;
    el.classList.remove('error-message', 'success-message');
    el.classList.add(variant);
    return el;
}

function setButtonLoading(button, isLoading, defaultLabel) {
    if (!button) return;
    button.disabled = isLoading;
    button.textContent = isLoading ? 'Signing In…' : defaultLabel;
}

function formatPrice(price) {
    return Number(price).toLocaleString('en-US', { maximumFractionDigits: 0 });
}

function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value == null ? '' : String(value);
    return div.innerHTML;
}

/* ---------- Cookie helpers ---------- */

function setCookie(name, value, days) {
    const maxAge = days * 24 * 60 * 60;
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
}
