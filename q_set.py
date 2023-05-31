from db_functions import run_search_query_tuples


def get_members(db_path):
    sql = """select 
    m.member_id, m.member_name, m.member_type, t.team_name as team, 
    m.email,m.dob, m.password, m.authorisation
    from member m
    left join team t on m.team_id = t.team_id
    order by team asc, member_name asc;"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return result


def get_class(db_path):
    sql="""select class_id, class_name, elevator_pitch, 
    content, start_date, frequency, duration 
    from class
    order by start_date asc"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return result


def get_class_registrations(class_id, db_path):
    sql = """select m.member_id, m.member_name, m.email, m.dob, r.attendance 
    from member m
    join registration r on m.member_id = r.member_id
    where r.class_id = ?
    order by m.member_name asc"""
    values_tuple = (class_id,)
    result = run_search_query_tuples(sql, values_tuple,db_path, True )
    return result

