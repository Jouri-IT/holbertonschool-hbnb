USE hbnb_db;

REPLACE INTO users (id, first_name, last_name, email, password, is_admin) 
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$omgd5ArmtQieR0a034cxdePjrdTzdIFpsRulfZdRGuEaTdQFm/v3u', 1);

REPLACE INTO amenities (id, name, description) 
VALUES (1, 'WiFi', ''), (2, 'Swimming Pool', ''), (3, 'Air Conditioning', '');
