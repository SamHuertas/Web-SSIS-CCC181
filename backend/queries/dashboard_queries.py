class DashboardQueries:
    
    GET_TOTAL_STUDENTS = """
        SELECT COUNT(*) as total_students FROM students;
    """
    
    GET_TOTAL_PROGRAMS = """
        SELECT COUNT(*) as total_programs FROM programs;
    """
    
    GET_TOTAL_COLLEGES = """
        SELECT COUNT(*) as total_colleges FROM colleges;
    """
    
    GET_STUDENTS_PER_COLLEGE = """
        SELECT 
            c.college_code, 
            c.college_name,
            COUNT(s.id_number) as student_count
        FROM colleges c
        LEFT JOIN programs p ON c.college_code = p.college_code
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY c.college_code, c.college_name
        ORDER BY student_count DESC
        LIMIT 7;
    """
    
    GET_TOP_PROGRAMS = """
        SELECT 
            p.program_code, 
            p.program_name,
            COUNT(s.id_number) as student_count
        FROM programs p
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY p.program_code, p.program_name
        ORDER BY student_count DESC
        LIMIT 7;
    """
    
    GET_COLLEGE_STATS = """
        SELECT 
            c.college_code, 
            c.college_name,
            COUNT(DISTINCT p.program_code) as program_count,
            COUNT(s.id_number) as student_count
        FROM colleges c
        LEFT JOIN programs p ON c.college_code = p.college_code
        LEFT JOIN students s ON p.program_code = s.program_code
        GROUP BY c.college_code, c.college_name
        ORDER BY student_count DESC;
    """
    
    GET_DASHBOARD_SUMMARY = """
        WITH student_counts AS (
            SELECT COUNT(*) as total_students FROM students
        ),
        program_counts AS (
            SELECT COUNT(*) as total_programs FROM programs
        ),
        college_counts AS (
            SELECT COUNT(*) as total_colleges FROM colleges
        ),
        students_per_college AS (
            SELECT 
                c.college_code, 
                c.college_name,
                COUNT(s.id_number) as student_count
            FROM colleges c
            LEFT JOIN programs p ON c.college_code = p.college_code
            LEFT JOIN students s ON p.program_code = s.program_code
            GROUP BY c.college_code, c.college_name
            ORDER BY student_count DESC
            LIMIT 7
        ),
        top_programs AS (
            SELECT 
                p.program_code, 
                p.program_name,
                COUNT(s.id_number) as student_count
            FROM programs p
            LEFT JOIN students s ON p.program_code = s.program_code
            GROUP BY p.program_code, p.program_name
            ORDER BY student_count DESC
            LIMIT 7
        )
        SELECT 
            (SELECT total_students FROM student_counts) as total_students,
            (SELECT total_programs FROM program_counts) as total_programs,
            (SELECT total_colleges FROM college_counts) as total_colleges,
            COALESCE(
                json_agg(
                    json_build_object(
                        'college_code', spc.college_code,
                        'college_name', spc.college_name,
                        'student_count', COALESCE(spc.student_count, 0)
                    )
                ),
                '[]'::json
            ) as students_per_college,
            COALESCE(
                json_agg(
                    json_build_object(
                        'program_code', tp.program_code,
                        'program_name', tp.program_name,
                        'student_count', COALESCE(tp.student_count, 0)
                    )
                ),
                '[]'::json
            ) as top_programs
        FROM students_per_college spc
        CROSS JOIN top_programs tp;
    """