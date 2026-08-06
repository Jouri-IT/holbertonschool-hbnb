INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$omgd5ArmtQieR0a034cxdePjrdTzdIFpsRulfZdRGuEaTdQFm/v3u',
    1,
    datetime('now'),
    datetime('now')
);

INSERT INTO amenities (name, description, created_at, updated_at)
VALUES
    ('Wifi', '', datetime('now'), datetime('now')),
    ('Swimming Pool', '' datetime('now'), datetime('now')),
    ('Air Conditioning', '', datetime('now'), datetime('now'));