-- 1. Search with pattern matching
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE (id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone_number
    FROM contacts c
    WHERE c.first_name ILIKE '%' || pattern || '%'
       OR c.last_name ILIKE '%' || pattern || '%'
       OR c.phone_number LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Pagination Function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone_number
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;