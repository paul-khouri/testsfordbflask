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


def get_registrations_members(db_path):
    """get all members and their registered classes (as inner dictionary)

    Returns : 2D list with inner dictionary for classes
    """
    sql = """ select m.member_name, c.class_name ,t.team_name, 
    m.member_type, m.email, m.dob
    from member m 
    left join registration r on m.member_id = r.member_id
    left join class c on c.class_id = r.class_id
    left join team t on t.team_id = m.team_id
    order by m.member_name asc"""

    result = run_search_query_tuples(sql,(), db_path, True)
    class_dict = {}
    class_names = get_class(db_path)
    for row in class_names:
        if row['class_name'] not in class_dict.keys():
            class_dict[ row['class_name'] ]=False
    print(class_dict)
    member={}
    member_name = ""
    registration_set = []
    for row in result:
        if row['member_name'] != member_name:
            member_name = row['member_name']
            member={}
            member['member_name'] = row['member_name']
            member['team_name'] = row['team_name']
            member['member_type'] = row['member_type']
            member['email'] = row['email']
            member['dob'] = row['dob']
            member['classes'] = class_dict.copy()
            registration_set.append(member)
        if row['class_name'] in member['classes'].keys():
            member['classes'][row['class_name']]=True
    return registration_set

