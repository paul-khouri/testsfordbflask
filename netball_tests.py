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





def get_dates(db_path):
    sql = """select strftime('%Y-%m-%d ', game_date) as "Date", strftime('%H:%M', game_date) as "Time", team_1, team_2 from game"""
    result = run_search_query_tuples(sql,(),db_path, True)
    for x in result:
        for k in x.keys():
            print(x[k], end=" , ")
        print()


def get_all(db_path):
    sql = """select * from game"""
    result = run_search_query_tuples(sql,(),db_path, True)
    for x in result:
        for k in x.keys():
            print(x[k], end=" , ")
        print()

def get_teams(db_path):
    sql = "select * from team"
    result = run_search_query_tuples(sql, (), db_path, True)
    output(result)




def get_matches(db_path):
    sql="""select match.match_date, team.team_name, match_team.points
    from match
    join match_team on match.match_id = match_team.match_id
    join team on match_team.team_id = team.team_id"""
    result = run_search_query_tuples(sql, (), db_path, True)
    for x in result:
        for k in x.keys():
            print(k, end=" : ")
            print(x[k], end=" , ")
        print()


def get_draw(db_path):
    sql = """ select d.draw_date as "Game Date", b.team_name as "Team 1", d.score_1 , c.team_name as "Team 2", d.score_2
    from draw d
    join team b on  d.team_1 = b.team_id
    join team c on  d.team_2 = c.team_id 
    where "Team 1" like 'Hot%' or c.team_name like 'Hot%'"""
    result = run_search_query_tuples(sql, (), db_path, True)
    output(result)









if __name__ == "__main__":
    db_path = 'data_netball/netball.sqlite'
    #get_all(db_path)
    #get_dates(db_path)
    #get_transpose()
    get_teams(db_path)
    #get_matches(db_path)
    #get_draw(db_path)