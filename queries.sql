-- 1. Competitions Analysis
-- 1.1 List all competitions with category names
SELECT c.competition_id, c.competition_name, cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id;

-- 1.2 Count the number of competitions in each category
SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_competitions DESC;

-- 1.3 Find competitions of type ‘doubles’
SELECT competition_id, competition_name, type
FROM competitions
WHERE type = 'doubles';

-- 1.4 Get competitions in a specific category (e.g., ITF Men)
SELECT c.competition_id, c.competition_name, c.type, cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 1.5 Identify parent competitions and their sub-competitions
SELECT p.competition_name AS parent_competition, c.competition_name AS sub_competition
FROM competitions c
JOIN competitions p ON c.category_id = p.category_id
WHERE c.competition_id <> p.competition_id;

-- 1.6 Analyze the distribution of competition types by category
SELECT cat.category_name, c.type, COUNT(c.competition_id) AS total
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name;

-- 1.7 List all top-level competitions (no parent)
SELECT competition_id, competition_name, type
FROM competitions
WHERE category_id IS NOT NULL;



-- 2. Venue Analysis
-- 2.1 List all venues along with their associated complex names
SELECT v.venue_id, v.venue_name, c.complex_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;

-- 2.2 Count the number of venues in each complex
SELECT c.complex_name, COUNT(v.venue_id) AS total_venues
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
GROUP BY c.complex_name
ORDER BY total_venues DESC;

-- 2.3 Get details of venues in a specific country
SELECT venue_id, venue_name, city_name, country_name
FROM venues
WHERE country_name = 'France';

-- 2.4 Identify all venues with their timezones
SELECT venue_id, venue_name, timezone
FROM venues
WHERE timezone IS NOT NULL;

-- 2.5 Find complexes with more than one venue
SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM complexes c
JOIN venues v ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

-- 2.6 List venues grouped by country
SELECT country_name, COUNT(venue_id) AS venue_count
FROM venues
GROUP BY country_name
ORDER BY venue_count DESC;

-- 2.7 Find all venues for a specific complex
SELECT v.venue_id, v.venue_name, v.city_name, v.country_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Melbourne Park';




-- 3. Competitor Ranking Analysis
-- 3.1 Get all competitors with their rank and points
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM competitor_rankings cr
JOIN competitors comp ON cr.competitor_id = comp.competitor_id
ORDER BY cr.rank_position ASC;

-- 3.2 Find competitors ranked in the top 5
SELECT comp.name, cr.rank_position, cr.points
FROM competitor_rankings cr
JOIN competitors comp ON cr.competitor_id = comp.competitor_id
WHERE cr.rank_position <= 5
ORDER BY cr.rank_position;

-- 3.3 List competitors with no rank movement (stable rank)
SELECT comp.name, cr.rank_position, cr.movement
FROM competitor_rankings cr
JOIN competitors comp ON cr.competitor_id = comp.competitor_id
WHERE cr.movement = 0;

-- 3.4 Get the total points of competitors from a specific country
SELECT comp.country, SUM(cr.points) AS total_points
FROM competitor_rankings cr
JOIN competitors comp ON cr.competitor_id = comp.competitor_id
WHERE comp.country = 'France';

-- 3.5 Count competitors per country
SELECT comp.country, COUNT(comp.competitor_id) AS competitor_count
FROM competitors comp
GROUP BY comp.country
ORDER BY competitor_count DESC;

-- 3.6 Find competitors with the highest points in the current week
SELECT comp.name, comp.country, cr.points
FROM competitor_rankings cr
JOIN competitors comp ON cr.competitor_id = comp.competitor_id
ORDER BY cr.points DESC
LIMIT 10;
