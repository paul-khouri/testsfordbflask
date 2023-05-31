from db_functions import run_search_query_tuples


def output(result):
    for x in result:
        for k in x.keys():
            print(k, end=" : ")
            print(x[k], end=" , ")
        print()

def get_transpose():
    L= [
        ["A",1],
        ["B", 1],
        ["C", 2],
        ["A", 2],
    ]
    D={}
    for x in L:
        if x[1] not in D.keys():
            D[x[1]] = [x[0]]
        else:
            D[x[1]].append(x[0])
    for x,y in D.items():
        print(x)
        print(y)


def get_schema(db_path):
    sql="""SELECT 
                name
            FROM 
                sqlite_master
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%';"""
    result = run_search_query_tuples(sql, (), db_path, False)
    print(result)





def get_teams(db_path):
    sql = "select * from team"
    result = run_search_query_tuples(sql, (), db_path, True)
    output(result)


def get_members(db_path):
    sql = """select 
    m.member_name, m.member_type, t.team_name as team, 
    m.email,m.dob, m.password, m.authorisation
    from member m
    left join team t on m.team_id = t.team_id
    order by team asc, member_name asc;"""
    result = run_search_query_tuples(sql, (), db_path, False)
    for x in result:
        print(x)


def get_draw(db_path):
    sql = """ select d.draw_date as "Game Date", b.team_name as "Team 1", d.score_1 , c.team_name as "Team 2", d.score_2
    from draw d
    join team b on  d.team_1 = b.team_id
    join team c on  d.team_2 = c.team_id 
    where "Team 1" like 'Hot%' or c.team_name like 'Hot%'"""
    result = run_search_query_tuples(sql, (), db_path, True)
    output(result)


def get_class(db_path):
    sql="""select class_id, class_name, elevator_pitch, 
    content, start_date, frequency, duration 
    from class"""
    result = run_search_query_tuples(sql, (), db_path, True)
    output(result)


def get_registrations(db_path):
    sql = """ select count(m.member_name), c.class_name, r.registration_date, 
    r.attendance 
    from member m 
    join registration r on m.member_id = r.member_id
    join class c on c.class_id = r.class_id
    group by c.class_name
    order by c.class_name asc"""
    result = run_search_query_tuples(sql,(), db_path, True)
    output(result)






if __name__ == "__main__":
    db_path = 'data_netball/netball.sqlite'

    #get_transpose()
    #get_teams(db_path)
    #get_draw(db_path)
    #get_schema(db_path)
    #get_members(db_path)
    #get_class(db_path)
    get_registrations(db_path)