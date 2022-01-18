CREATE DATABASE shopify_db;
USE shopify_db;

CREATE TABLE inventory (
	inventoryId MEDIUMINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    code VARCHAR(128) NOT NULL,
    type VARCHAR(32) NOT NULL,
    supplier VARCHAR(128) NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
	description VARCHAR(512),
    createdTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    modifiedTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (inventoryId)
);