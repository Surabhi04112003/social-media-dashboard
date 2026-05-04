CREATE DATABASE social_db;
USE social_db;
SHOW TABLES;
SELECT * FROM social_data LIMIT 10;
SELECT COUNT(*) FROM social_data;
DESCRIBE social_data;
SELECT SUM(total_engagement) AS total_engagement FROM social_data;
SELECT AVG(likes) AS avg_likes FROM social_data;
SELECT platform, COUNT(*) AS total_posts
FROM social_data
GROUP BY platform
ORDER BY total_posts DESC;
SELECT platform, SUM(total_engagement) AS engagement
FROM social_data
GROUP BY platform
ORDER BY engagement DESC;
SELECT location, COUNT(*) AS total
FROM social_data
GROUP BY location
ORDER BY total DESC;