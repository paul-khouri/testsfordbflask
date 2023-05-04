from db_functions import run_search_query_tuples


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





if __name__ == "__main__":
    db_path = 'data_netball/netball.sqlite'
    #get_all(db_path)
    #get_dates(db_path)
    get_transpose()