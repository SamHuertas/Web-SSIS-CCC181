class AuthQueries:
    
    INSERT_USER = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING user_id, username, email;
    """
    
    FIND_USER_BY_EMAIL = """
        SELECT user_id, username, email, password_hash
        FROM users
        WHERE email = %s;
    """
    
    FIND_USER_BY_ID = """
        SELECT user_id, username, email
        FROM users
        WHERE user_id = %s;
    """