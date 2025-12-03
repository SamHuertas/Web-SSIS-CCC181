class CollegeQueries:

    FIND_ALL = """
        SELECT college_code, college_name
        FROM colleges;
    """
    
    FIND_BY_CODE = """
        SELECT college_code, college_name
        FROM colleges
        WHERE college_code = %s;
    """
    
    INSERT = """
        INSERT INTO colleges (college_code, college_name)
        VALUES (%s, %s)
        RETURNING college_code, college_name;
    """
    
    UPDATE = """
        UPDATE colleges
        SET college_code = %s, college_name = %s
        WHERE college_code = %s
        RETURNING college_code, college_name;
    """
    
    DELETE = """
        DELETE FROM colleges
        WHERE college_code = %s
        RETURNING college_code, college_name;
    """
    
    GET_STATS = """
        SELECT 
            c.college_code, 
            c.college_name, 
            COUNT(DISTINCT p.program_code) AS program_count,
            COUNT(s.id_number) AS student_count
        FROM colleges c
        LEFT JOIN programs p ON c.college_code = p.college_code
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY c.college_code, c.college_name
        ORDER BY student_count DESC;
    """