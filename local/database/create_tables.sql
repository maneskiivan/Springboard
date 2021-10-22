CREATE DATABASE springboard_venues;

USE springboard_venues;

CREATE TABLE venue(
	id INT NOT NULL AUTO_INCREMENT,
    venue_name VARCHAR(500) NOT NULL,
    canonical_url VARCHAR(500) DEFAULT NULL,
    verified BOOLEAN,
    url VARCHAR(500) DEFAULT NULL,
    likes INT DEFAULT 0,
    rating FLOAT DEFAULT 0,
    venue_desc VARCHAR(1000) DEFAULT NULL,
    herenow INT DEFAULT 0,
    days VARCHAR(20) DEFAULT NULL,
    createdat DATETIME DEFAULT NULL,
    photos INT DEFAULT 0,
    tips INT DEFAULT 0,
    listed INT DEFAULT NULL,
    PRIMARY KEY (id)
    );
    
CREATE TABLE contact(
	contact_id INT NOT NULL AUTO_INCREMENT,
    phone VARCHAR(50) DEFAULT NULL,
    formattedPhone VARCHAR(100) DEFAULT NULL,
    twitter VARCHAR(100) DEFAULT NULL,
    instagram VARCHAR(100) DEFAULT NULL,
    facebook VARCHAR(100) DEFAULT NULL,
    facebookUsername VARCHAR(100) DEFAULT NULL,
    facebookName VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (contact_id)
    );
    
ALTER TABLE venue
ADD COLUMN contact_id INT NOT NULL;
    
ALTER TABLE venue
ADD FOREIGN KEY (contact_id) REFERENCES contact (contact_id);

CREATE TABLE location(
	location_id INT NOT NULL AUTO_INCREMENT,
    address VARCHAR(100) DEFAULT NULL,
    crossStreet VARCHAR(100) DEFAULT NULL,
    neighborhood VARCHAR(100) DEFAULT NULL,
    lat VARCHAR(50) DEFAULT NULL,
    lng VARCHAR(50) DEFAULT NULl,
    postalCode VARCHAR(100) DEFAULT NULL,
    cc VARCHAR(5) DEFAULT NULL,
    city VARCHAR(50) DEFAULT NULL,
    state VARCHAR(50) DEFAULT NULL,
    country VARCHAR(50) DEFAULT NULL,
    formattedAddress VARCHAR(500) DEFAULT NULL,
    PRIMARY KEY (location_id)
    );

ALTER TABLE venue
ADD COLUMN location_id INT NOT NULL;
    
ALTER TABLE venue
ADD FOREIGN KEY (location_id) REFERENCES location (location_id);

CREATE TABLE stats(
	id INT NOT NULL AUTO_INCREMENT,
    checkinCount INT DEFAULT 0,
    usersCount INT DEFAULT 0,
    tipCount INT DEFAULT 0,
    visitsCount INT DEFAULT 0,
    PRIMARY KEY (id)
    );
    
ALTER TABLE venue
ADD COLUMN stats_id INT NOT NULL;
    
ALTER TABLE venue
ADD FOREIGN KEY (stats_id) REFERENCES stats (id);

CREATE TABLE price(
	id INT NOT NULL AUTO_INCREMENT,
    currency VARCHAR(10) DEFAULT NULL,
    message VARCHAR(100) DEFAULT NULL,
    tier INT DEFAULT 0,
    PRIMARY KEY (id)
    );

ALTER TABLE venue
ADD COLUMN price_id INT NOT NULL;
    
ALTER TABLE venue
ADD FOREIGN KEY (price_id) REFERENCES price (id);

CREATE TABLE attributes(
	venue_id INT NOT NULL,
    name VARCHAR(50),
    FOREIGN KEY (venue_id) REFERENCES venue (id)
    );
    
CREATE TABLE category(
	id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    prim BOOLEAN DEFAULT 0,
	PRIMARY KEY (id)
    );

CREATE TABLE categories(
	venue_id INT NOT NULL,
    category_id INT NOT NULL
    );
    
ALTER TABLE categories
ADD FOREIGN KEY (venue_id) REFERENCES venue (id),
ADD FOREIGN KEY (category_id) REFERENCES category (id)



