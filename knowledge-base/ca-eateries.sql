-- This is SQL ++
-- Bucket: travel-sample
-- Scope: inventory
-- Collection: landmark

SELECT 
    l.name, 
    l.content, 
    l.price, 
    l.url, 
    l.geo, 
    l.phone
FROM 
    landmark AS l
WHERE 
    l.state = "California" AND 
    l.activity = "eat" AND
    l.name IS NOT NULL AND
    l.content IS NOT NULL AND
    l.price IS NOT NULL AND
    l.url IS NOT NULL AND
    l.geo IS NOT NULL AND
    l.phone IS NOT NULL;

-- Returns: 187 Restaurants