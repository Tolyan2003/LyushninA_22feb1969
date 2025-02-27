CREATE TABLE categories (
    category_id  INTEGER PRIMARY KEY,
    name         VARCHAR(255),
    description  VARCHAR(255)
);

CREATE TABLE regions (
    region_id    INTEGER PRIMARY KEY,
    name         VARCHAR(255),
    description  TEXT,
    size         DECIMAL(10, 2)
);

CREATE TABLE mushrooms (
    mushroom_id      INTEGER PRIMARY KEY,
    name             VARCHAR(255),
    description      TEXT,
    season           VARCHAR(255),
    edible           BOOLEAN,
    category_id      INTEGER,
    primary_region_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (primary_region_id) REFERENCES regions(region_id)
);