DROP DATABASE IF EXISTS potty_map;

CREATE DATABASE potty_map;

\c potty_map
CREATE TABLE users (
    id serial PRIMARY KEY,
    full_name text NOT NULL,
    email text NOT NULL UNIQUE,
    username text NOT NULL UNIQUE,
    password text NOT NULL
);

CREATE TABLE bathrooms (
    id serial PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    zip_code text NOT NULL,
    longitude text NOT NULL,
    latitude text NOT NULL,
    website text,
    added_by text REFERENCES users (username)
);

INSERT INTO users (full_name, email, username, PASSWORD)
    VALUES ('Eddie Z', 'eddie@zeta.com', 'Eddie', '$2b$12$8ZyEYe2PtS9zQvnmKW03EOJH/k3gDJMVo14vSXWHH5tXwcJrxq4VO');

