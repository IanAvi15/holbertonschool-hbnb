-- =============================================================
-- HBnB Evolution — Database Schema and Initial Data
-- =============================================================

-- -------------------------------------------------------------
-- Table: users
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          CHAR(36)        PRIMARY KEY,
    first_name  VARCHAR(255)    NOT NULL,
    last_name   VARCHAR(255)    NOT NULL,
    email       VARCHAR(255)    NOT NULL UNIQUE,
    password    VARCHAR(255)    NOT NULL,
    is_admin    BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------------
-- Table: places
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS places (
    id          CHAR(36)        PRIMARY KEY,
    title       VARCHAR(255)    NOT NULL,
    description TEXT,
    price       DECIMAL(10, 2)  NOT NULL,
    latitude    FLOAT           NOT NULL,
    longitude   FLOAT           NOT NULL,
    owner_id    CHAR(36)        NOT NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- -------------------------------------------------------------
-- Table: amenities
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS amenities (
    id          CHAR(36)        PRIMARY KEY,
    name        VARCHAR(255)    NOT NULL UNIQUE,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------------
-- Table: reviews
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    id          CHAR(36)        PRIMARY KEY,
    text        TEXT            NOT NULL,
    rating      INT             NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id     CHAR(36)        NOT NULL,
    place_id    CHAR(36)        NOT NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- -------------------------------------------------------------
-- Table: place_amenity  (many-to-many join table)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id    CHAR(36)        NOT NULL,
    amenity_id  CHAR(36)        NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- =============================================================
-- Initial Data
-- =============================================================

-- Administrator user
-- Password: admin1234  (bcrypt2 hash below)
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$.sRyseAGY9ARmbh5cmYhkuSUbd1UFz9lquw6sTs.tGX7TznTk4QcC',
    TRUE
);

-- Initial amenities
INSERT INTO amenities (id, name) VALUES
    ('a95de28b-e1a2-4f52-ab2e-c5ed90093a18', 'WiFi'),
    ('7bce1083-4cb3-46bf-8e11-21e3a398cd89', 'Swimming Pool'),
    ('5ecb1591-0620-44a2-8015-f48fa95f9893', 'Air Conditioning');