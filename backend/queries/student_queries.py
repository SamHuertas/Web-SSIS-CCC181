class StudentQueries:
    
    FIND_ALL = """
        SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
        FROM students;
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