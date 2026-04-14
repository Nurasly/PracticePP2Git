def search_contacts():
    term = input("Search by name or phone prefix: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s", (f'%{term}%', f'{term}%'))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()