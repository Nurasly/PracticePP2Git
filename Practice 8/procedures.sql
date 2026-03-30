-- 1. Upsert Procedure (Insert or Update if exists)
CREATE OR REPLACE PROCEDURE upsert_contact(p_fname TEXT, p_lname TEXT, p_phone TEXT)
AS $$
BEGIN
    INSERT INTO contacts (first_name, last_name, phone_number)
    VALUES (p_fname, p_lname, p_phone)
    ON CONFLICT (phone_number) 
    DO UPDATE SET first_name = p_fname, last_name = p_lname;
END;
$$ LANGUAGE plpgsql;

-- 2. Bulk Insert with Validation
-- Returns a list of failed phone numbers via the INOUT parameter
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names TEXT[], 
    p_surnames TEXT[], 
    p_phones TEXT[],
    INOUT failed_phones TEXT[] DEFAULT ARRAY[]::TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        -- Simple validation: phone must be at least 7 characters
        IF length(p_phones[i]) >= 7 THEN
            INSERT INTO contacts (first_name, last_name, phone_number)
            VALUES (p_names[i], p_surnames[i], p_phones[i])
            ON CONFLICT DO NOTHING;
        ELSE
            failed_phones := array_append(failed_phones, p_phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- 3. Delete Procedure
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_identifier TEXT)
AS $$
BEGIN
    DELETE FROM contacts 
    WHERE first_name = p_identifier OR phone_number = p_identifier;
END;
$$ LANGUAGE plpgsql;