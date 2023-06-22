from db_functions import run_search_query_tuples, file_reader


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


def get_registrations_members(db_path):
    sql = """ select m.member_name, c.class_name ,t.team_name, 
    m.member_type, m.email, m.dob
    from member m 
    join registration r on m.member_id = r.member_id
    join class c on c.class_id = r.class_id
    left join team t on t.team_id = m.team_id
    order by m.member_name asc"""

    result = run_search_query_tuples(sql,(), db_path, True)
    output(result)
    class_dict = {}
    for row in result:
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
    for r in registration_set:
        print(r)
    #output(result)


def file_reader_test():
    csv_path = 'data_netball/members.csv'
    collected_data = file_reader(csv_path)
    collected_data.pop(0)
    #for row in collected_data:
        #print(row[0])



if __name__ == "__main__":
    db_path = 'data_netball/netball.sqlite'
    file_reader_test()

    #get_transpose()
    #get_teams(db_path)
    #get_draw(db_path)
    #get_schema(db_path)
    #get_members(db_path)
    #get_class(db_path)
    get_registrations_members(db_path)