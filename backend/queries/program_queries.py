class ProgramQueries:
    
    FIND_ALL_WITH_COLLEGE = """
        SELECT p.program_code, p.program_name, p.college_code, c.college_name
        FROM programs p
        LEFT JOIN colleges c ON p.college_code = c.college_code;
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