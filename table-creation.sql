-- creating database 
CREATE DATABASE sport_radar;
USE sport_radar;


-- Categories
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(50),
    type VARCHAR(100)
);


-- Competitions
CREATE TABLE competitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    gender VARCHAR(50),
    parent_id INT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES competitions(id) ON DELETE SET NULL
);


-- Complexes
CREATE TABLE complexes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country_name VARCHAR(100),
    country_code VARCHAR(10)
);


-- Venues
CREATE TABLE venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country_name VARCHAR(100),
    timezone VARCHAR(100),
    complex_id INT,
    FOREIGN KEY (complex_id) REFERENCES complexes(id) ON DELETE CASCADE
);



-- Competitors
CREATE TABLE competitors (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(100),
    country_code VARCHAR(10),
    abbreviation VARCHAR(10)
);



-- Competitor_Rankings
CREATE TABLE competitor_rankings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rank_position INT NOT NULL,
    movement INT,
    points INT,
    competitions_played INT,
    competitor_id VARCHAR(100),
    FOREIGN KEY (competitor_id) REFERENCES competitors(id) ON DELETE CASCADE
);


SELECT * FROM categories;

SELECT COUNT(*) FROM competitions;

SELECT * FROM competitor_rankings;

SELECT * FROM competitors;

SELECT * FROM complexes;

SELECT * FROM venues;



