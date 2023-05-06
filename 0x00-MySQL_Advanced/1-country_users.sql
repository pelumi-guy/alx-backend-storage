-- A SQL script that creates a table (called users) with following fields
-- id, email, name, country (enumeration of countries: US, CO and TN)
CREATE TABLE IF NOT EXISTS users (
	id int NOT NULL AUTO_INCREMENT,
	email varchar(255) NOT NULL,
	name varchar(255),
	country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL,
	UNIQUE (email),
	PRIMARY KEY (id)
	);
