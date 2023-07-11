DROP DATABASE IF EXISTS potty_map;

CREATE DATABASE potty_map;

\c potty_map
CREATE TABLE users(
    id serial PRIMARY KEY,
    full_name text NOT NULL,
    email text NOT NULL UNIQUE,
    username text NOT NULL UNIQUE DEFAULT 'Admin',
    password text NOT NULL
);

CREATE TABLE bathrooms(
    id serial PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    zip_code text NOT NULL,
    longitude text NOT NULL,
    latitude text NOT NULL,
    website text,
);

INSERT INTO users(full_name, email, username, PASSWORD)
    VALUES ('Eddie Z', 'eddie@zeta.com', 'Eddie', '$2y$12$OKPBu639rqXuhpTAb70Fj.DGmAG/YDD/KQdkqvi6AYG0sWZoStYV.');

INSERT INTO bathrooms(name, address, zip_code, longitude, latitude, website)
    VALUES ('My House', '1036 N Dearborn St', '60610', '-87.63011829999999', '41.9016931', 'bjbproperties.com')
