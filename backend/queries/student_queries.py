class StudentQueries:
    
    FIND_ALL = """
        SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
        FROM students
        ORDER BY {sort_field} {sort_direction}
        LIMIT %s OFFSET %s;
    """
    
    COUNT_ALL = """
        SELECT COUNT(*) as total
        FROM students;
    """
    
    FIND_ALL_SEARCH = """
        SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
        FROM students
        WHERE 
            (LOWER(id_number) LIKE %s OR
            LOWER(first_name) LIKE %s OR
            LOWER(last_name) LIKE %s OR
            LOWER(program_code) LIKE %s OR
            CAST(year_level AS TEXT) LIKE %s)
            {filter_clause}
        ORDER BY {sort_field} {sort_direction}
        LIMIT %s OFFSET %s;
    """
    
    COUNT_ALL_SEARCH = """
        SELECT COUNT(*) as total
        FROM students
        WHERE 
            (LOWER(id_number) LIKE %s OR
            LOWER(first_name) LIKE %s OR
            LOWER(last_name) LIKE %s OR
            LOWER(program_code) LIKE %s OR
            CAST(year_level AS TEXT) LIKE %s)
            {filter_clause};
    """
    
    FIND_ALL_FILTER = """
        SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
        FROM students
        WHERE 1=1
            {filter_clause}
        ORDER BY {sort_field} {sort_direction}
        LIMIT %s OFFSET %s;
    """
    
    COUNT_ALL_FILTER = """
        SELECT COUNT(*) as total
        FROM students
        WHERE 1=1
            {filter_clause};
    """
    
    FIND_BY_ID = """
        SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
        FROM students
        WHERE id_number = %s;
    """
    
    INSERT = """
        INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code, picture)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
    """
    
    UPDATE = """
        UPDATE students
        SET id_number = %s, first_name = %s, last_name = %s, year_level = %s, 
            gender = %s, program_code = %s, picture = %s
        WHERE id_number = %s
        RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
    """
    
    DELETE = """
        DELETE FROM students
        WHERE id_number = %s
        RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
    """
    
    GET_STUDENTS_PER_PROGRAM = """
        SELECT p.program_code, p.program_name, COUNT(s.id_number) AS student_count
        FROM programs p
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY p.program_code, p.program_name
        ORDER BY student_count DESC;
    """
    
    GET_ALL_PROGRAMS = """
        SELECT program_code, program_name
        FROM programs
        ORDER BY program_name ASC;
    """