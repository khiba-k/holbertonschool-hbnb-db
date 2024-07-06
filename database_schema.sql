CREATE DATABASE IF NOT EXISTS hbtn_0e_6_usa;

USE hbtn_0e_6_usa;


-- Create the States table first
CREATE TABLE States (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Then create the Users table
CREATE TABLE Users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Then create the Places table
CREATE TABLE Places (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Then create the Reviews table
CREATE TABLE Reviews (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES Places(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Then create the Amenities table
CREATE TABLE Amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Then create the Cities table with reference to States
CREATE TABLE Cities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    state_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES States(id)
);
