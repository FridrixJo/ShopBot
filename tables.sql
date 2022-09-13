CREATE TABLE users
(
    user_id VARCHAR PRIMARY KEY NOT NULL,
    name    VARCHAR
);

CREATE TABLE statement
(
    id         INTEGER PRIMARY KEY,
    menu       VARCHAR,
    work_text  VARCHAR,
    support    VARCHAR,
    btc_wallet VARCHAR
);

INSERT INTO statement (id, menu, work_text, support, btc_wallet) VALUES(1, 'Main menu', 'Work', 'Support', 'jfuh734u3j9duih4fujf8j3948jf3');

CREATE TABLE requests
(
    request_id  VARCHAR     PRIMARY KEY     NOT NULL,
    user_id     VARCHAR,
    name        VARCHAR
);

CREATE TABLE products
(
    name        VARCHAR     PRIMARY KEY     NOT NULL,
    description VARCHAR,
    photo_id    VARCHAR
);

CREATE TABLE locations
(
    location VARCHAR    PRIMARY KEY     NOT NULL
);

CREATE TABLE categories
(
    name     VARCHAR    NOT NULL,
    category VARCHAR    NOT NULL,
    price    VARCHAR
);

alter table users
    owner to postgres;

alter table statement
    owner to postgres;

alter table requests
    owner to postgres;

alter table locations
    owner to postgres;

alter table products
    owner to postgres;

alter table categories
    owner to postgres;






