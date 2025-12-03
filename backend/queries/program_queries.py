class ProgramQueries:
    
    FIND_ALL = """
        SELECT p.program_code, p.program_name, p.college_code, c.college_name
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code
        ORDER BY {sort_field} {sort_direction}
        LIMIT %s OFFSET %s;
    """
    
    COUNT_ALL = """
        SELECT COUNT(*) as total
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code;
    """
    
    FIND_ALL_SEARCH = """
        SELECT p.program_code, p.program_name, p.college_code, c.college_name
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE 
            LOWER(p.program_code) LIKE %s OR
            LOWER(p.program_name) LIKE %s OR
            LOWER(p.college_code) LIKE %s OR
            LOWER(c.college_name) LIKE %s
        ORDER BY {sort_field} {sort_direction}
        LIMIT %s OFFSET %s;
    """
    
    COUNT_ALL_SEARCH = """
        SELECT COUNT(*) as total
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE 
            LOWER(p.program_code) LIKE %s OR
            LOWER(p.program_name) LIKE %s OR
            LOWER(p.college_code) LIKE %s OR
            LOWER(c.college_name) LIKE %s;
    """
    
    FIND_BY_CODE = """
        SELECT program_code, program_name, college_code
        FROM programs
        WHERE program_code = %s;
    """
    
    INSERT = """
        INSERT INTO programs (program_code, program_name, college_code)
        VALUES (%s, %s, %s)
        RETURNING program_code, program_name, college_code;
    """
    
    UPDATE = """
        UPDATE programs
        SET program_code = %s, program_name = %s, college_code = %s
        WHERE program_code = %s
        RETURNING program_code, program_name, college_code;
    """
    
    DELETE = """
        DELETE FROM programs
        WHERE program_code = %s
        RETURNING program_code, program_name, college_code;
    """